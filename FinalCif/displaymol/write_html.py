

def write(moldata: str, width: int = 240, height: int = 240):
    m = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <script src="jquery.min.js"></script>
    <script src="JSmol_dk.nojq.lite.js"></script>
    
    <!-- 
    A template to display molecules with JSmol Lite.
    --> 
    """ + r"""
    <!-- MOL DATA
    {}
    -->
    """.format(moldata) + r"""
    
    <script type="text/javascript"> 
    
    
    $(window).ready(function() {
      var Info;
      Info = {
      """ + """
          width: {},
          height: {},
          """.format(width, height) + r"""
          color: "0xFFFFFF",
          shadeAtoms: false,
          addSelectionOptions: false,
          use: "HTML5",
          readyFunction: null,
          defaultModel: "",
          bondWidth: 2,
          zoomScaling: 8,
          pinchScaling: 6.0,
          mouseDragFactor: 0.7,
          touchDragFactor: 0.15,
          multipleBondSpacing: 0,
          spinRateX: -0.08,
          spinRateY: 0.05,
          spinFPS: 20,
          spin: false,
          debug: false,
          infodiv: false,
          j2sPath: "."
      };
      Jmol._document = null;
      Jmol.getTMApplet("jmol", Info);
      $("#apphere").html(jmol._code);
      var mol = $('html').html().split("MOL DATA\n")[1].split("-->")[0];
      jmol.__loadModel(mol);
    });

    </script>
    </head>
    <body>

    <div id="apphere"></div>

    </body>
    </html>
    """
    return m
