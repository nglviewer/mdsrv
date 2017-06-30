<!DOCTYPE html>
<html>

  <head>
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
    <meta name="description" content="MDsrv : MD trajectory server">

    <link rel="stylesheet" type="text/css" media="screen" href="stylesheets/stylesheet.css">
		<style>
      table, td, th { border: 0 solid black; }
    </style>
    <title>MDsrv</title>
  </head>

  <body>

<!-- HEADER AND SIDEBAR -->
<?php include 'include/headerSide.php';?>

<div class="content">

<br>

<p align=justify>In order to deploy the MDsrv, an html file has to be generated. We generated a working sample <a target="_blank" href="data/mdsrv.html">mdsrv.html</a> file and will explain parts of it here. The complete file is also presented <a href="webapp.html#default_html">below</a>.</p>

<h2><a id="js" class="anchor" href="#jas" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>JavaScript inclusion</h2>
<pre><code>&lt!-- NGL --&gt
    &ltscript src="mdsrv/webapp/js/ngl.js"&gt&lt/script&gt
&lt!-- UI --&gt
    &ltscript src="mdsrv/webapp/js/lib/signals.min.js"&gt&lt/script&gt
    ...
&lt!-- MDSRV --&gt
    &ltscript src="mdsrv/webapp/js/mdsrv.js"&gt&lt/script&gt
</code></pre>
<p align=justify>The NGL and MDsrv scripts have to be made available by including them within the &ltscript&gt&lt/script&gt tag. The source of the files depends on the deployment directory, which corresponds to the folder, where the <em>mdsrv.wsgi</em> is located, normally in <em>/var/www/mdsrv</em>.</p>


<h2><a id="ngldefiniton" class="anchor" href="#ngldefinition" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>MDsrv/ngl definitions</h2>
<pre><code>// Datasources
NGL.DatasourceRegistry.add(
	"file", new MdsrvDatasource( window.location.origin + "/mdsrv/" )
);
NGL.DatasourceRegistry.listing = NGL.DatasourceRegistry.get( "file" );
NGL.DatasourceRegistry.trajectory = NGL.DatasourceRegistry.get( "file" );</code></pre>

<p align=justify><em>DatasourceRegistry</em> defines the source of the data files (structures and trajectories), which is defined within the <em>app.cfg</em>. The source of the configuration file is defined within the <em>/var/www/mdsrv/mdsrv.wsgi</em>. The naming (here 'file') is used furthermore within the .js/.ngl scripts and the url for loading files (e.g http://localhost:8000/index.html?load=<strong>file</strong>://MDsrv/script.ngl) </p>

<br>
<pre><code>var load = NGL.getQuery( "load" );
if( load ) stage.loadFile( load, { defaultRepresentation: true } );
var struc = NGL.getQuery( "struc" );
var traj = NGL.getQuery( "traj" );
if( struc ){
	var params = { defaultRepresentation: true };
	stage.loadFile( struc, params ).then( function( o ){
		if( traj ) o.addTrajectory( traj );
	} );
}</code></pre>
<p align=justify>Additionally, other flags as loading, structure and trajectory with a similar usage as for 'file' can be defined and renamed (e.g http://localhost:8000/webapp/?<strong>struc</strong>=file://cwd/md.gro&<strong>traj</strong>=file://cwd/md.gro).</p>



<h2><a id="default_html" class="anchor" href="#default_html" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Default example html file</h2>
<pre><code>&lt!DOCTYPE html&gt
&lthtml lang="en"&gt
&lthead&gt
    &lttitle&gtNGL/MDsrv&lt/title&gt

    &ltmeta charset="utf-8"&gt
    &ltmeta name="viewport" content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0"&gt

    &ltlink rel="icon" href="favicon.ico" type="image/x-icon"/&gt
    &ltlink rel="stylesheet" href="mdsrv/webapp/css/font-awesome.min.css" /&gt
    &ltlink rel="stylesheet" href="mdsrv/webapp/css/main.css" /&gt
    &ltlink rel="subresource" href="mdsrv/webapp/css/light.css" /&gt
    &ltlink rel="subresource" href="mdsrv/webapp/css/dark.css" /&gt
&lt/head&gt
&ltbody&gt
    &lt!-- NGL --&gt
    &ltscript src="mdsrv/webapp/js/ngl.js"&gt&lt/script&gt

    &lt!-- UI --&gt
    &ltscript src="mdsrv/webapp/js/lib/signals.min.js"&gt&lt/script&gt
    &ltscript src="mdsrv/webapp/js/lib/tether.min.js"&gt&lt/script&gt
    &ltscript src="mdsrv/webapp/js/lib/colorpicker.min.js"&gt&lt/script&gt
    &ltscript src="mdsrv/webapp/js/ui/ui.js"&gt&lt/script&gt
    &ltscript src="mdsrv/webapp/js/ui/ui.extra.js"&gt&lt/script&gt
    &ltscript src="mdsrv/webapp/js/ui/ui.ngl.js"&gt&lt/script&gt
    &ltscript src="mdsrv/webapp/js/ui/ui.helper.js"&gt&lt/script&gt
    &ltscript src="mdsrv/webapp/js/gui.js"&gt&lt/script&gt

    &lt!-- MDSRV --&gt
    &ltscript src="mdsrv/webapp/js/mdsrv.js"&gt&lt/script&gt

    &ltscript&gt
        NGL.cssDirectory = "mdsrv/webapp/css/";
        NGL.documentationUrl = "http://arose.github.io/ngl/api/";

        // Datasources
        NGL.DatasourceRegistry.add(
            "file", new MdsrvDatasource( window.location.origin + "/mdsrv/" )
        );
        NGL.DatasourceRegistry.listing = NGL.DatasourceRegistry.get( "file" );
        NGL.DatasourceRegistry.trajectory = NGL.DatasourceRegistry.get( "file" );
        document.addEventListener( "DOMContentLoaded", function(){
            stage = new NGL.Stage();
            NGL.StageWidget( stage );

            var load = NGL.getQuery( "load" );
            if( load ) stage.loadFile( load, { defaultRepresentation: true } );

            var struc = NGL.getQuery( "struc" );
            var traj = NGL.getQuery( "traj" );
            if( struc ){
                var params = { defaultRepresentation: true };
                stage.loadFile( struc, params ).then( function( o ){
                    if( traj ) o.addTrajectory( traj );
                } );
            }
        } );
    &lt/script&gt
&lt/body&gt
&lt/html&gt</code></pre>


<h1>
<a id="more" class="anchor" href="#more" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>More</h1>

<p>If you have question, feel free to use the
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
