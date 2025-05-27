from blacksheep import Response
from blacksheep.contents import Content

from scraper.configs.openapidocs import docs
from scraper.routes.routers import base


@docs(
    responses={200: "Lyrics page displayed successfully"},
    description="Display lyrics for Bad Religion's Punk Rock Song",
    tags=["Lyrics"],
)
@base.get("/")
async def punk_rock_song_lyrics():
    """Display Bad Religion's Punk Rock Song lyrics"""
    
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bad Religion - Punk Rock Song</title>
        <style>
            body {
                font-family: 'Courier New', monospace;
                background: linear-gradient(135deg, #000000, #1a1a1a);
                background-image: url('https://guitar.com/wp-content/uploads/2022/12/bad-religion-getty@2000x1500.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                color: #ffffff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
            
            .container {
                max-width: 800px;
                padding: 40px;
                background: rgba(0, 0, 0, 0.9);
                border: 2px solid #ff0000;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
                text-align: center;
            }
            
            .header {
                margin-bottom: 30px;
            }
            
            .band-name {
                font-size: 3em;
                font-weight: bold;
                color: #ff0000;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
                margin: 0;
            }
            
            .song-title {
                font-size: 2em;
                color: #ffffff;
                margin: 10px 0;
                text-transform: uppercase;
                letter-spacing: 2px;
            }
            
            .lyrics {
                font-size: 1.2em;
                line-height: 1.8;
                text-align: left;
                margin: 30px 0;
                padding: 20px;
                background: rgba(0, 0, 0, 0.1);
                border-radius: 5px;
            }
            
            .verse {
                margin-bottom: 20px;
            }
            
            .chorus {
                font-weight: bold;
                color: #ff6666;
                margin: 25px 0;
                padding: 15px;
                background: rgba(255, 0, 0, 0.1);
                border-radius: 5px;
            }
            
            .footer {
                margin-top: 30px;
                font-size: 0.9em;
                color: #cccccc;
                font-style: italic;
            }
            
            .punk-accent {
                color: #ff0000;
                font-weight: bold;
            }
            
            @keyframes pulse {
                0% { text-shadow: 0 0 5px rgba(255, 0, 0, 0.5); }
                50% { text-shadow: 0 0 20px rgba(255, 0, 0, 0.8); }
                100% { text-shadow: 0 0 5px rgba(255, 0, 0, 0.5); }
            }
            
            .band-name {
                animation: pulse 2s infinite;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 class="band-name">BAD RELIGION</h1>
                <h2 class="song-title">Punk Rock Song</h2>
            </div>
            
            <div class="lyrics">
                <div class="verse">
                    Have you been to the desert?<br>
                    Have you walked with the dead?<br>
                    There's a <span class="punk-accent">hundred thousand reasons</span><br>
                    To be going instead<br>
                    Many miles you have been<br>
                    From your <span class="punk-accent">soul's inner dreams</span><br>
                    Pull it out, turn around<br>
                    There's a face in the ground
                </div>
                
                <div class="chorus">
                    It's a <span class="punk-accent">punk rock song</span><br>
                    Written for the people who can see something's wrong<br>
                    Like ants in marching<br>
                    We go along with their ways<br>
                    And time stands still for no one<br>
                    And so we die young and we pray
                </div>
                
                <div class="verse">
                    Have you been to the desert?<br>
                    Have you walked with the dead?<br>
                    There's a <span class="punk-accent">hundred thousand reasons</span><br>
                    To be going instead<br>
                    Many miles you have been<br>
                    From your <span class="punk-accent">soul's inner dreams</span><br>
                    Pull it out, turn around<br>
                    There's a face in the ground
                </div>
                
                <div class="chorus">
                    It's a <span class="punk-accent">punk rock song</span><br>
                    Written for the people who can see something's wrong<br>
                    Like ants in marching<br>
                    We go along with their ways<br>
                    And time stands still for no one<br>
                    And so we die young and we pray
                </div>
                
                <div class="verse">
                    Have you been to the desert?<br>
                    Have you walked with the dead?<br>
                    There's a <span class="punk-accent">hundred thousand reasons</span><br>
                    To be going instead<br>
                    Many miles you have been<br>
                    From your <span class="punk-accent">soul's inner dreams</span>
                </div>
            </div>
            
            <div class="footer">
                <p>© Bad Religion - "Punk Rock Song" from the album <em>Against the Grain</em> (1990)</p>
                <p>🎸 <span class="punk-accent">PUNK'S NOT DEAD</span> 🎸</p>
            </div>
        </div>
    </body>
    </html>
    """
    

    return Response(
        200,
        [(b"content-type", b"text/html; charset=utf-8")],
        Content(b"text/html", html_content.encode("utf-8"))
    )
