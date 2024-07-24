import streamlit as st
import json
import os

st.set_page_config(
    page_title="The Mosaic Mind of AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for fonts and body
st.markdown('<style>div.block-container{padding-top:0.5rem;}</style>', unsafe_allow_html=True)

white_color = "#fff"
h1 = "1.8rem"
h2 = "1.5rem"
h3 = "1.1rem"
p = "0.9rem"

font_css = f"""
<style>
    body {{
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: black;
        color: white;
    }}
    .title-box {{
        padding: 10px;
        margin: 10px;
        background-color: #333;
        color: {white_color};
        border-radius: 10px;
        box-shadow: 0.4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease-in-out;
    }}
    h1 {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: {h1};
        font-weight: bold;
        font-stretch: condensed;
        margin: 0;
        letter-spacing: 0.08rem;
    }}
    h2 {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: {h2};
        font-weight: bold;
        font-stretch: condensed;
        letter-spacing: 0.02rem;
    }}
    h3 {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: {h3};
        font-weight: bold;
        font-stretch: condensed;
        letter-spacing: 0.01rem;
        color: #edcce8;
    }}
    h5, p {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        color: #85888c;
        font-size: {p};
    }}
    @media (max-width: 480px) {{
        .title-box {{
            padding: 10px;
            margin: 10px;
        }}
        h1 {{
            font-size: 1.4rem;
        }}
    }}
    h2 {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: {h2};
        font-weight: bold;
        font-stretch: condensed;
        letter-spacing: 0.02rem;
    }}
    h3 {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        font-size: {h3};
        font-weight: bold;
        font-stretch: condensed;
        letter-spacing: 0.01rem;
    }}
    h5, p {{
        font-family: 'Helvetica Neue', Arial, sans-serif !important;
        color: #dbdbdb;
        font-size: {p};
    }}
</style>
"""

st.markdown(font_css, unsafe_allow_html=True)

# Facebook network GNN

# Read the JSON graph data
@st.cache_data 
def load_network_data():
    json_file_path = 'network_data.json'
    with open(json_file_path, 'r') as json_file:
        network_data = json.load(json_file)
    return network_data

network_data = load_network_data()

# Convert JSON data to string and insert it directly into the HTML template
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Social Network</title>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            overflow: hidden;
        }}

        #mynetwork {{
            width: 100%;
            height: 100vh;
            border: none;
        }}

        h1 {{
            position: absolute;
            font-weight: bold;
            text-align: center;
            left: 50px;
            top: 0px;
            color: white;
            font-size: 30px;
            z-index:10;
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: bold;
            font-stretch: condensed; 
        }}

        .spinner {{
            border: 16px solid #f3f3f3; /* Light grey */
            border-top: 16px solid #dab6db; /* Pink */
            border-radius: 50%;
            width: 80px;
            height: 80px;
            animation: spin 2s linear infinite;
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
        }}

        @keyframes spin {{
            0% {{ transform: translate(-50%, -50%) rotate(0deg); }}
            100% {{ transform: translate(-50%, -50%) rotate(360deg); }}
        }}


        .progress {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 20px;
            color: white;
            z-index: 1000;
        }}


    </style>
</head>
<body>
<div class="spinner"></div> <!-- Spinner added here -->
<div class="progress">0%</div> <!-- Added this div -->
<div id="mynetwork"></div>
<script>
    document.addEventListener('DOMContentLoaded', function () {{
        const container = document.getElementById('mynetwork');
        const spinner = document.querySelector('.spinner'); // Access the spinner
        const progressText = document.querySelector('.progress');
        const data = {json.dumps(network_data)};
        const options = {{
            nodes: {{
                shape: 'dot',
                size: 40,
                font: {{
                    size: 22,
                    color: 'white',
                }}
            }},
            edges: {{
                width: 5
            }},
            physics: {{
                barnesHut: {{
                    gravitationalConstant: -30000
                }}
            }}
        }};

        // Initialize the network
        const network = new vis.Network(container, data, options);

       // Hide spinner when the network is ready
        network.on("stabilizationIterationsDone", function () {{
            spinner.style.display = 'none';
        }});

        let progress = 0;
            const interval = setInterval(() => {{
                progress += 10;
                if (progress <= 100) {{
                    progressText.innerText = `${{progress}}%`;
                }} else {{
                    clearInterval(interval);
                }}
            }}, 300);

            network.on("stabilizationIterationsDone", function () {{
                clearInterval(interval);
                progressText.style.display = 'none';
            }});

        // Ensure that the network fits well within the container when resized
        window.addEventListener('resize', function () {{
            network.fit(); 
        }});
    }});
</script>
</body>
</html>
"""

def main():
    st.title("Facebook Social Network GNN Visualization")
    st.subheader("Collection of ML Projects Created by [Fay Cai](https://www.faycai.com)")
    st.write("More Info about this [GNN model](https://www.faycai.com/data-science/the-mosaic-mind-of-ai-app)")
    st.components.v1.html(html_content, height=800, scrolling=True)

if __name__ == '__main__':
    main()
