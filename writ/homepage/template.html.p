<!doctype html>

<html class="no-js" lang="">

<head>
  <meta charset="utf-8">
  <title></title>
  <meta name="description" content="">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <meta property="og:title" content="">
  <meta property="og:type" content="">
  <meta property="og:url" content="">
  <meta property="og:image" content="">

  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" href="/icon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="icon.png">

  <link rel="stylesheet" href="css/remedy.css">
  <link rel="stylesheet" href="css/style.css">
  <link rel="stylesheet" href="fonts/fonts.css" />

  <link rel="manifest" href="site.webmanifest">
  <meta name="theme-color" content="#fafafa">
</head>
<body>
◊(->html doc)
The current page is called ◊|here|.
◊(define prev-page (previous here))
◊when/splice[prev-page]{The previous is <a href="◊|prev-page|">◊|prev-page|</a>.}
◊(define next-page (next here))
◊when/splice[next-page]{The next is <a href="◊|next-page|">◊|next-page|</a>.}
</body>
<!--
  <script src="js/vendor/modernizr-3.12.0.min.js"></script>
  <script src="js/app.js"></script>
 -->
</html>
