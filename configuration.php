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

<h1>
<a id="configuration" class="anchor" href="#configuration" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>MDsrv configuration</h1>

<p align=justify>The MDsrv settings can be modified by changing the <em>app.cfg</em> file, downloadable <a target="_blank" href="data/app.cfg">here</a>. Please find a permanent secure location (not accessible by others) for the file. It is possible to change the host and port, the list of directories where you store your structure and trajectory files (<em>DATA_DIRS</em>) and the security settings. The file is written in Python</p>

<h4><a id="datadir" class="anchor" href="#datadir" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>DATA_DIRS</h4>
<p align=justify>
Directories where simulations are located should be listed within the <em>DATA_DIR</em> dictionary. It contains only directories, no links to specific files. There is no limit to reuse directories or division into several subdirectories.
can be hidden with an underscore (e.g. <em>"_secrets": os.path.abspath("/mnt/disk1/projects")</em>) and only accessed via the url with the directory name (e.g. <em>_secrets</em>).  </p>
<pre><code>DATA_DIRS = {
	"_hidden": os.path.abspath("/path/hidden/from/dir/listing"),
	"myproject": os.path.abspath("/path/project"),
}</code></pre>
<br>
<h4><a id="settings" class="anchor" href="#settings" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Security settings</h4>
<p align=justify>
MDsrv provides two possible ways to secure the data:
<ul><li><em>REQUIRE_AUTH</em> protects all directories defined in <em>DATA_DIRS</em> with a user and a passphrase.</li>
<li><em>REQUIRE_DATA_AUTH</em> secures the single directories individually with an username and a password. </li></ul>
<pre><code>REQUIRE_AUTH = False
USERNAME = "user"
PASSWORD = "pass"

REQUIRE_DATA_AUTH = True
DATA_AUTH = {
	"_hidden2": [ "user", "test123" ],
	"myproject": [ "user", "test123" ],
}</code></pre>
Note that only one of <em>REQUIRE_AUTH</em> and <em>REQUIRE_DATA_AUTH</em> can be true with the former taken precedence.
  </p>
<p align=justify><strong>Additional settings:</strong>
<br>
Within the configuration file, <em>HOST</em> and <em>PORT</em> can be set.
<br>
Whenever the <a target="_blank" href="data/app.cfg">app.cfg</a> file is changed, the apache server has to be restarted. If content within the directories is changed, a restart is not necessary. To restart execute one of the following commants

<pre><code>sudo /etc/init.d/apache2 restart
sudo service apache2 restart
</code></pre>
</p>




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


  </body>
</html>