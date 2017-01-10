/**
 * @file UI HELPER
 * @author Alexander Rose <alexander.rose@weirdbyte.de>
 */

var unicodeHelper = function(){

    var replace_map = {
        "{alpha}": "\u03B1",
        "{beta}": "\u03B2",
        "{gamma}": "\u03B3",
        "{dot}": "\u00B7",
        "{bullet}": "\u2022",
    }

    var keys = Object.keys( replace_map ).join('|');

    var rg = new RegExp( '(' + keys + ')', 'gi' );

    return function( str ){

        return str.replace(
            rg, function( s, p1, p2, offset, sx ){
                return replace_map[ String( s ) ];
            }
        );

    };

}();


function scriptHelperFunctions( stage, panel ){

    var U = unicodeHelper;

    //

    function components( name ){

        return stage.getComponentsByName( name );

    }

    function representations( name ){

        return stage.getRepresentationsByName( name );

    }

    function structures( name ){

        return stage.getComponentsByName( name, NGL.StructureComponent );

    }

    //

    function color( value, collection ){

        collection.setColor( value );

    }

    function visibility( value, collection ){

        collection.setVisibility( value );

    }

    function hide( collection ){

        visibility( false, collection );

    }

    function show( collection, only ){

        if( only ) hide();

        visibility( true, collection );

    }

    function superpose( comp1, comp2, align, sele1, sele2, xsele1, xsele2 ){

        comp1.superpose( comp2, align, sele1, sele2, xsele1, xsele2 );

    }

    //

    function uiText( text, newline ){

        var elm = new UI.Text( U( text ) );

        panel.add( elm );

        if( newline ) uiBreak( 1 );

        return elm;

    }

    function uiHtml( html, newline ){

        var elm = new UI.Html( U( html ) );

        panel.add( elm );

        if( newline ) uiBreak( 1 );

        return elm;

    }

    function uiBreak( n ){

        n = n === undefined ? 1 : n;

        for( var i = 0; i < n; ++i ){

            panel.add( new UI.Break() );

        }

    }

    function uiButton( label, callback ){

        var btn = new UI.Button( U( label ) ).onClick( function(){
            callback( btn );
        } );

        panel.add( btn );

        return btn;

    }

    function uiSelect( options, callback ){

        if( Array.isArray( options ) ){
            var newOptions = {};
            options.forEach( function( name ){
                newOptions[ name ] = name;
            } );
            options = newOptions;
        }

        var select = new UI.Select()
            .setOptions( options )
            .onChange( function(){
                callback( select );
            } );

        panel.add( select );

        return select;

    }

/*
    function uiOpenButton( label, callback, extensionList ){

        var btn = new UI.Button( U( label ) ).onClick( function(){

            NGL.open( callback, extensionList );

        } );

        panel.add( btn );

        return btn;

    }
*/

    function uiDownloadButton( label, callback, downloadName ){

        var btn = new UI.Button( U( label ) ).onClick( function(){

            NGL.download( callback, downloadName );

        } );

        panel.add( btn );

        return btn;

    }

    function uiVisibilitySelect( collection ){

        var list = collection.list;

        function getVisible(){

            var nameList = [];

            list.forEach( function( o ){

                if( o.visible ) nameList.push( o.name );

            } );

            return nameList;

        }

        var options = { "": "[show]" };

        list.forEach( function( o ){

            options[ o.name ] = o.name;

            o.signals.visibilityChanged.add( function(){

                var nameList = getVisible();

                if( nameList.length === list.length ){
                    select.setValue( "" );
                }else if( o.visible ){
                    select.setValue( o.name );
                }else{
                    select.setValue( nameList[ 0 ] );
                }

            } );

        } );

        var select = new UI.Select()
            .setOptions( options )
            .onChange( function(){

                var name = select.getValue();

                if( name === "" ){
                    show( collection );
                }else{
                    hide( collection );
                    show( stage.getAnythingByName( name ) );
                }

            } );

        panel.add( select );

        return select;

    }

    function uiVisibilityButton( label, collection ){

        label = U( label ? label : "all" );
        collection = collection || new NGL.Collection();

        if( !( collection instanceof NGL.Collection ) &&
            !( collection instanceof NGL.ComponentCollection ) &&
            !( collection instanceof NGL.RepresentationCollection )
        ){
            collection = new NGL.Collection( [ collection ] );
        }

        var list = collection.list;

        function isVisible(){

            var visible = false;

            list.forEach( function( o ){

                if( o.visible ) visible = true;

            } );

            return visible;

        }

        function getLabel( value ){

            return ( isVisible() ? "hide " : "show " ) + label;

        }

        list.forEach( function( o ){

            o.signals.visibilityChanged.add( function(){

                btn.setLabel( getLabel() );

            } );

        } );

        var btn = new UI.Button( getLabel() ).onClick( function(){

            visibility( !isVisible(), collection );

        } );

        // panel.add( btn );

        return btn;

    }

    function uiPlayButton( label, trajComp, step, timeout, start, end ){

        var traj = trajComp.trajectory;
        label = U( label );

        var player = new NGL.TrajectoryPlayer( traj, step, timeout, start, end );
        player.mode = "once";

        var btn = new UI.Button( "play " + label )
            .onClick( function(){
                player.toggle();
            } );

        player.signals.startedRunning.add( function(){
            btn.setLabel( "pause " + label );
        } );

        player.signals.haltedRunning.add( function(){
            btn.setLabel( "play " + label );
        } );

        panel.add( btn );

        return btn;

    }

    //

    return {

        'components': components,
        'representations': representations,
        'structures': structures,

        'color': color,
        'visible': visibility,
        'hide': hide,
        'show': show,
        'superpose': superpose,

        'uiText': uiText,
        'uiHtml': uiHtml,
        'uiBreak': uiBreak,
        'uiSelect': uiSelect,
        'uiButton': uiButton,
        //'uiOpenButton': uiOpenButton,
        'uiDownloadButton': uiDownloadButton,
        'uiVisibilitySelect': uiVisibilitySelect,
        'uiVisibilityButton': uiVisibilityButton,
        'uiPlayButton': uiPlayButton,

    };

};
