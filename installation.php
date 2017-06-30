<!DOCTYPE html>
<html>

  <head>
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
    <meta name="description" content="MDsrv : MD trajectory server">

    <link rel="stylesheet" type="text/css" media="screen" href="stylesheets/stylesheet.css">

    <title>MDsrv</title>
  </head>

  <body>

<!-- HEADER AND SIDEBAR -->
<?php include 'include/headerSide.php';?>

<div class="content">
          <h1><a id="installation" class="anchor" target="_blank" href="#installation" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Installation</h1>

<p align=justify>The latest stable release of MDsrv can be easily installed via PyPI.</p>

<pre><code>pip install mdsrv
</code></pre>
<br>
<p align=justify>To install the development version, download it from the
<a target="_blank" href="https://github.com/arose/mdsrv/releases">MDsrv GitHub page</a> and install it manually (via executing <em>setup.py</em> within the repository). Pip needs to be installed in advance to add underlying tools otherwise an installation error (e.g. "import setuptools not found") might rise.
<br>
For further information, consult the <em>setuptools</em> <a target="_blank" href="http://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode">documentation</a> .
</p>

<h3>Operating systems</h3>
<p align=justify>The MDsrv has been tested and can be installed on Linux and Mac OS. Windows support is currently under development.</p>
<p align=justify>The deployed NGL sessions can be viewed on every operating system and browser which supports WebGL.</p>

<h3>Deployment</h3>
<p align=justify>In order to add the MDsrv into your daily research, deploy and configure it to your system and your settings. The advantage is that you can add project folders permanently, including their security settings. Additionally, you can add a link to your cluster and inspect your unprocessed simulations remotely. By setting up an apache server (locally on your machine or global on a webserver), you are able to share your sessions and files with colleagues within the same network, collaborators or reviewers.</p>
<p align=justify>To get information how to do this, inspect the <a href="deployment.html">deployment guide</a>.</p>

<h1>
<a id="more" class="anchor" href="#more" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>More</h1>

<p>If you have questions concerning the installation, feel free to use the
<a target="_blank" href="https://github.com/arose/mdsrv/issues">Issue Tracker</a> or write a mail to
<a href="mailto:johanna.tiemann@gmail.com">johanna.tiemann@gmail.com</a> or
<a href="mailto:alexander.rose@weirdbyte.de">alexander.rose@weirdbyte.de</a>.</p>

<p>Please give us <strong>feedback</strong>!</p>

    </div>
    </div>
    
<!-- FOOTER  -->
<?php include 'include/footer.php';?>
    </div>



  </body>
</html>
