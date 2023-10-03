#lang pollen

strace -e open,openat a -l acme_python |& grep Compose
◊;(require pollen/unstable/pygments)

◊(define (highlight lang . xs)
   `(pre (code ((class ,(format "~a" lang))) ,@xs)))


How to build a simple vector search app

◊todo{explain vector search}

http://jsomers.net/blog/dictionary
◊link["https://github.com/websterParser/WebsterParser"]{clean}

	dict.json which we ◊link[]{clean}

◊link["https://www.dropbox.com/s/w62l6pdfl8dtw2z/webst.json?dl=0"]{webst.json}
(65MB)

◊link["https://github.com/mye/simple-vector-search/blob/main/cleanwebst.py"]{cleaning script}

◊highlight['bash]{
python cleanwebst.py <../webst.json > cleanwebst.json
}

◊highlight['python]{
for x in range(3):
    print x
}

◊highlight['bash]{
for x in range(3):
    print x
}

Compute the sentence embeddings

Prepare an sqlite database for the dictionary

Insert dictionary and embeddings into sqlite

Search for matches with [ScaNN](https://github.com/google-research/google-research/tree/master/scann)


Try it now with

◊highlight['bash]{
curl ...
}

◊todo{ What did I learn?

PyArrow tables and embeddings aren't a great fit
I lost an afternoon fiddling
Did it help me write this article?

}

◊jobsearch{
}

