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

    <!-- NGL -->
    <script src="data/mdsrv/webapp/js/ngl.js"></script>

    <!-- UI -->
    <script src="data/mdsrv/webapp/js/lib/signals.min.js"></script>
    <script src="data/mdsrv/webapp/js/lib/tether.min.js"></script>
    <script src="data/mdsrv/webapp/js/lib/colorpicker.min.js"></script>
    <script src="data/mdsrv/webapp/js/ui/ui.js"></script>
    <script src="data/mdsrv/webapp/js/ui/ui.extra.js"></script>
    <script src="data/mdsrv/webapp/js/ui/ui.ngl.js"></script>
    <script src="data/mdsrv/webapp/js/ui/ui.helper.js"></script>
    <script src="data/mdsrv/webapp/js/gui.js"></script>

    <!-- MDSRV -->
    <script src="data/mdsrv/webapp/js/mdsrv.js"></script>

    <script>
        NGL.cssDirectory = "data/mdsrv/webapp/css/";
        NGL.documentationUrl = "http://arose.github.io/ngl/api/";

        // Datasources
        NGL.DatasourceRegistry.add(
            "file", new MdsrvDatasource( window.location.origin + "/mdsrv/" )
        );
        NGL.DatasourceRegistry.listing = NGL.DatasourceRegistry.get( "file" );
        NGL.DatasourceRegistry.trajectory = NGL.DatasourceRegistry.get( "file" );
        document.addEventListener( "DOMContentLoaded", function(){
            stage = new NGL.Stage( "viewport" );
            stage.loadFile( "data/md.gro", { defaultRepresentation: true, asTrajectory: true } ).then( function( comp ){
        	    comp.setName( "simulation-name" );
	            comp.setSelection( "protein and not #h" );
							comp.addRepresentation( "licorice", {visible: false} );
							comp.addTrajectory( );

	        } );
            var toggleTheme = document.getElementById( "toggleTheme" );
            var isLight = false;
            toggleTheme.addEventListener( "click", function(){
		        if( !isLight ){
                    stage.setParameters( { backgroundColor: "white" } );
                    isLight = true;
                }else{
                    stage.setParameters( { backgroundColor: "black" } );
                    isLight = false;
                }
            } );
            var toggleSpin = document.getElementById( "toggleSpin" );
            var isSpinning = false;
            toggleSpin.addEventListener( "click", function(){
                if( !isSpinning ){
                    stage.setSpin( [ 0, 1, 0 ], 0.01 );
                    isSpinning = true;
                }else{
                    stage.setSpin( null, null );
                    isSpinning = false;
                }
            } );
            var toggleLicorice = document.getElementById( "toggleLicorice" );
            toggleLicorice.addEventListener( "click", function(){
							stage.getRepresentationsByName( "licorice" ).list.forEach( function( repre ){
									repre.setVisibility( !repre.visible );
							} );
            } );
            var toggleRunMDs = document.getElementById( "toggleRunMDs" );
            var isRunning = false;
            toggleRunMDs.addEventListener( "click", function(){
				var trajComp = stage.getComponentsByName("simulation-name").list[0].trajList[0];
				var player = new NGL.TrajectoryPlayer(trajComp.trajectory, {timeout: 200});
				if( !isRunning ){
					player.play();
					isRunning = true;
				}else{
			   	 player.play();
					player.pause();
					isRunning = false;
				}
            } );

        } );
    </script>



<!-- HEADER AND SIDEBAR -->
<?php include 'include/headerSide.php';?>

<div class="content">


<br>

<p align=justify>The example for an embedded html provided below loads a .gro trajectory with cartoon representation as trajectory into the embedded NGL viewer and generates a button below to play/pause the simulation. The parameters set within the <em>component.trajectory</em> representation are overwritten (or set back to default) by the trajectory player. We now explain some parts of the html file in detail.</p>


<p align=justify>The JavaScript inclusion is explained <a href="webapp.html">elsewhere</a>. It has also to be specified here in order to use the MDsrv.</p>

<pre><code>&ltscript&gt
document.addEventListener( "DOMContentLoaded", function(){
	stage = new NGL.Stage( "viewport" );
	stage.loadFile( "/mdsrv/file/data/md.gro", { asTrajectory: true } )
	.then(function( o){
		o.addRepresentation( "cartoon", { sele: "protein" } );
		o.addTrajectory();
		o.centerView();
	} );
} );
&lt/script&gt

&ltdiv id="viewport" style="width:800px; height:800px;"&gt&lt/div&gt</code></pre>

<p align=justify>A new stage 'viewport' is created and inserted into the web page. Files and simulations including their representations and settings can then be loaded into the stage. More features for the structures are explained within the <a href="basicscripting.html">basic scripting</a> section.</p>
<br>
<pre><code>document.addEventListener( "DOMContentLoaded", function(){
	var togglePlayer = document.getElementById( "playerButton" );
	var playing = false;
	togglePlayer.addEventListener( "click", function(){
		var trajComp = stage.getComponentsByName("md.gro").list[0].trajList[0];
		var player = new NGL.TrajectoryPlayer(
			trajComp.trajectory, { step: 1, timeout: 200 }
		);
		if( !playing ){
			player.play();
			playing = true;
		}else{
			player.play();
			player.pause();
			playing = false;
		}
	} );
} );

&ltdiv style="width:500px;"&gt
	&ltbutton id="playerButton"&gtplay/pause&lt/button&gt
&lt/div&gt</code></pre>

<p align=justify>Functional buttons as a play/pause button can also be defined. First a new event has to be created including a <em>TrajectoryPlayer</em>, afterwards, the function has to be defined. This is just a short example, more can be found in the <a href="advanced.html">advanced scripting</a> section.</p>



<h2><a id="embedded_example" class="anchor" href="#embedded_example" aria-hidden="true"><span aria-hidden="true" class="octicon octicon-link"></span></a>Embedded html example</h2>

<pre><code>&lt!DOCTYPE html&gt
&lthtml lang="en"&gt
&lthead&gt
    &lttitle&gtMDsrv/NGL - embedded&lt/title&gt

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
            stage = new NGL.Stage( "viewport" );
            stage.loadFile( "/mdsrv/file/data/md.gro", { asTrajectory: true } )
            .then(function( o){
                o.addRepresentation( "cartoon", { sele: "protein" } );
                o.addTrajectory();
                o.centerView();
            } );
            var togglePlayer = document.getElementById( "playerButton" );
            var playing = false;
            togglePlayer.addEventListener( "click", function(){
                var trajComp = stage.getComponentsByName("md.gro").list[0].trajList[0];
                var player = new NGL.TrajectoryPlayer(trajComp.trajectory, {step: 1, timeout: 200});
                if( !playing ){
                    player.play();
                    playing = true;
                }else{
                    player.play();
                    player.pause();
                    playing = false;
                }
            } );
        } );
    &lt/script&gt
    &ltdiv id="viewport" style="width:800px; height:800px;"&gt&lt/div&gt
    &ltdiv style="width:500px;"&gt
        &ltbutton id="playerButton"&gtplay/pause&lt/button&gt
    &lt/div&gt
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
