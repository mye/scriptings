import PIL, numpy as np, torch, json

from hashlib import blake2b
from pathlib import Path

def resize_image(image):
	w0, h0 = image.size
	ratio, wide = (512 / w0, True) if w0 >= h0 else (512 / h0, False)
	w, h = (512, ratio * h0) if wide else (ratio * w0, 512)
	w, h = (x - x % 32 for x in map(int, (w, h)))  # resize to integer multiple of 32
	return image.resize((w, h), resample=PIL.Image.Resampling.LANCZOS)


def image_tensor(image) -> torch.Tensor:
	image = np.array(image).astype(np.float32) / 255.0
	image = image[None].transpose(0, 3, 1, 2)
	image = torch.from_numpy(image)
	return 2.0 * image - 1.0


def load_image(filename):
	pil_image0 = PIL.Image.open(filename).convert("RGB")
	pil_image1 = resize_image(pil_image0)
	init_tensor = image_tensor(pil_image1)
	return init_tensor


def save_image(image, prompt, negative_prompt, seed, steps, guidance, strength, outdir=Path('.'), quality=90):
	w, h = image.size
#	prompt_digest = blake2b(bytes(prompt + negative_prompt, 'utf-8')).hexdigest()[:6]
	prompt_digest = blake2b(image.tobytes()).hexdigest()[:6]
	name_parts = [prompt_digest, seed, f"{w}x{h}", steps, guidance, strength]
	outdir = Path(outdir)
	outdir.mkdir(exist_ok=True, parents=True)
	if not (prompt_file := outdir / f'{prompt_digest}.txt').exists():
		prompt_file.write_text(prompt + "\n" + negative_prompt)
	filename = "_".join(map(str, name_parts)) + ".jpg"
	path = outdir / filename
	image.save(path)
	return path


def embed_text(pipe, prompt, negative_prompt="") :
	text_tokens = pipe.tokenizer(prompt,
		padding="max_length",
		max_length=pipe.tokenizer.model_max_length,
		truncation=True,
		return_tensors="pt")
	max_length = text_tokens.input_ids.shape[-1]
	uncond_input = pipe.tokenizer([negative_prompt], padding="max_length", max_length=max_length, return_tensors="pt")
	uncond_embeddings = pipe.text_encoder(uncond_input.input_ids.to(pipe.device))[0]
	text_embeddings = pipe.text_encoder(text_tokens.input_ids.to(pipe.device))[0]
	text_embeddings = torch.cat([uncond_embeddings, text_embeddings])
	return text_embeddings


@torch.no_grad()
@torch.autocast('cuda')
def iterate(pipe, latents, t_index, time, text_embeddings, guidance_scale=7.5):
	# expand the latents for classifier free guidance
	latent_model_input = torch.cat([latents] * 2)
	sigma = pipe.scheduler.sigmas[t_index]
	# the model input needs to be scaled to match the continuous ODE formulation in K-LMS
	latent_model_input = latent_model_input / ((sigma**2 + 1) ** 0.5)
	latent_model_input = latent_model_input.to(pipe.unet.dtype)
	time = time.to(pipe.unet.dtype)
	# predict the noise residual
	noise_pred = pipe.unet(latent_model_input, time, encoder_hidden_states=text_embeddings).sample
	# guidance
	noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
	noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_text - noise_pred_uncond)
	return pipe.scheduler.step(noise_pred, t_index, latents).prev_sample


def dict_from_line(line: "JSON dict line") -> dict:
	try:
		d = json.loads(line)
	except json.JSONDecodeError:
		d = None  # ignore invalid lines
	return d
