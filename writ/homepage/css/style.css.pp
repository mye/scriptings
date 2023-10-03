#lang pollen

◊(require css-tools/column css-tools/core css-tools/transition)

◊(make-media-query 23 11 1000 40)

◊(define default-margin "2.5rem")
◊(define paragraph-space "0.8rem")
◊(define anchor-hover-color "hsla(30, 20%, 90%, 1)")

html {
/*
  color: #222;
  font-size: 1em;
  line-height: 1.4;
*/
}

body {
  position: relative; ◊; this establishes body as reference container
  padding: 0;
  margin-left: auto;
  margin-right: auto;
  width:100%;
  max-width:1000px;
  min-width:520px;
  min-height: 100%;
  ◊(make-css-kerning)
  ◊(make-css-ligatures)
  color: #444;
  -webkit-font-smoothing: subpixel-antialiased; /* corrects safari rendering */
}

p {
  line-height: 1.4;
  margin-bottom: ◊|paragraph-space|;
}

h1, .home-link {
  text-transform: uppercase;
  font-family: "cooper-hewitt";
  font-size: 2rem;
  line-height: 1.1;
}

::-moz-selection {
  background: #b3d4fc;
  text-shadow: none;
}

::selection {
  background: #b3d4fc;
  text-shadow: none;
}

hr {
  display: block;
  height: 1px;
  border: 0;
  border-top: 1px solid #ccc;
  margin: 1em 0;
  padding: 0;
}

fieldset {
  border: 0;
  margin: 0;
  padding: 0;
}

textarea {
  resize: vertical;
}



.chapter {
  font-family: "cooper-hewitt";
  text-transform: uppercase;
  letter-spacing: 0.07rem;
  margin-top: 2.5rem;
  font-size: 2rem;
  margin-bottom: 5rem;
}

.mono {
	font-family: "fira-mono";
}

.margin-note {
  font-size: 82%;
  margin-bottom: 1rem; ◊; prevents two asides from adjacency
  font-family: "fira-sans";
  line-height: 1.35;
  color: #666;
}



th {
	font-family: "fira-sans";
	font-variant-caps: all-small-caps;
	font-feature-settings: 'c2sc' 1;
	font-weight: normal;
	text-transform: lowercase;
	font-size: 85%;
	padding: 0.3rem 0.5rem 0.3rem 0.5rem;
	line-height: 1.05;
}


/* ==========================================================================
   Helper classes
   ========================================================================== */

/*
 * Hide visually and from screen readers
 */

.hidden,
[hidden] {
  display: none !important;
}

/*
 * Hide only visually, but have it available for screen readers:
 * https://snook.ca/archives/html_and_css/hiding-content-for-accessibility
 *
 * 1. For long content, line feeds are not interpreted as spaces and small width
 *    causes content to wrap 1 word per line:
 *    https://medium.com/@jessebeach/beware-smushed-off-screen-accessible-text-5952a4c2cbfe
 */

.visually-hidden {
  border: 0;
  clip: rect(0, 0, 0, 0);
  height: 1px;
  margin: -1px;
  overflow: hidden;
  padding: 0;
  position: absolute;
  white-space: nowrap;
  width: 1px;
  /* 1 */
}

/*
 * Extends the .visually-hidden class to allow the element
 * to be focusable when navigated to via the keyboard:
 * https://www.drupal.org/node/897638
 */

.visually-hidden.focusable:active,
.visually-hidden.focusable:focus {
  clip: auto;
  height: auto;
  margin: 0;
  overflow: visible;
  position: static;
  white-space: inherit;
  width: auto;
}

/*
 * Hide visually and from screen readers, but maintain layout
 */

.invisible {
  visibility: hidden;
}

/*
 * Clearfix: contain floats
 *
 * The use of `table` rather than `block` is only necessary if using
 * `::before` to contain the top-margins of child elements.
 */

.clearfix::before,
.clearfix::after {
  content: "";
  display: table;
}

.clearfix::after {
  clear: both;
}

/* ==========================================================================
   EXAMPLE Media Queries for Responsive Design.
   These examples override the primary ('mobile first') styles.
   Modify as content requires.
   ========================================================================== */

@media only screen and (min-width: 35em) {
  /* Style adjustments for viewports that meet the condition */
}

@media print,
  (-webkit-min-device-pixel-ratio: 1.25),
  (min-resolution: 1.25dppx),
  (min-resolution: 120dpi) {
  /* Style adjustments for high resolution devices */
}

/* ==========================================================================
   Print styles.
   Inlined to avoid the additional HTTP request:
   https://www.phpied.com/delay-loading-your-print-css/
   ========================================================================== */

@media print {
  *,
  *::before,
  *::after {
    background: #fff !important;
    color: #000 !important;
    /* Black prints faster */
    box-shadow: none !important;
    text-shadow: none !important;
  }

  a,
  a:visited {
    text-decoration: underline;
  }

  a[href]::after {
    content: " (" attr(href) ")";
  }

  abbr[title]::after {
    content: " (" attr(title) ")";
  }

  /*
   * Don't show links that are fragment identifiers,
   * or use the `javascript:` pseudo protocol
   */
  a[href^="#"]::after,
  a[href^="javascript:"]::after {
    content: "";
  }

  pre {
    white-space: pre-wrap !important;
  }

  pre,
  blockquote {
    border: 1px solid #999;
    page-break-inside: avoid;
  }

  tr,
  img {
    page-break-inside: avoid;
  }

  p,
  h2,
  h3 {
    orphans: 3;
    widows: 3;
  }

  h2,
  h3 {
    page-break-after: avoid;
  }
}

