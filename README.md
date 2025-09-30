<h1 align="center">CodeFolio - Your Personal Coding Profile Aggregator</h1>

<p align="center">
<img src="https://img.shields.io/badge/Django-5.2-darkgreen.svg" alt="Django Version">
<img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python Version">
<img src="https://img.shields.io/badge/Selenium-4.3-green.svg" alt="Selenium">
<img src="https://img.shields.io/badge/Bootstrap-5.3-purple.svg" alt="Bootstrap">
</p>

CodeFolio is a full-stack web application built with Django, designed to fetch, aggregate, and display a developer's problem-solving statistics from online coding platforms. It uses a powerful web scraping engine to dynamically pull data from a user's LeetCode profile in real-time.

The application features a secure, custom-built authentication system with email-based OTP verification. Once logged in, users are presented with a personal dashboard where they can input their LeetCode handle to instantly view a comprehensive breakdown of their solved problems, language proficiency, skill tags, and yearly activity.

<!-- <h2>Table of Contents</h2>
<ol>
<li><a href="#features">Features</a></li>
<li><a href="#project-structure">Project Structure</a></li>
<li><a href="#setup-and-installation">Setup and Installation</a></li>
<li><a href="#running-the-application">Running the Application</a></li>
<li><a href="#future-improvements">Future Improvements</a></li>
</ol> -->

<h2 id="features">✨ Features</h2>

<ul>
<li><strong>Dynamic Web Scraper:</strong>
<ul>
<li>Utilizes <strong>Selenium</strong> to control a headless Chrome browser, allowing it to execute JavaScript and wait for dynamic content to load on LeetCode profiles.</li>
<li>Intelligently interacts with the page by locating and clicking "Show more" buttons to reveal all data before parsing.</li>
<li>Uses <strong>BeautifulSoup</strong> to accurately parse the rendered HTML and extract a wide range of statistics.</li>
</ul>
</li>
<li><strong>Secure Email-Based Authentication:</strong>
<ul>
<li>A stylish, responsive registration and login system where users are identified by their email address.</li>
<li>Prevents duplicate registrations by validating against existing emails.</li>
</ul>
</li>
<li><strong>Time-Sensitive OTP Verification:</strong>
<ul>
<li>Secures new accounts by sending a 6-digit verification code to the user's email upon registration.</li>
<li>The code and pending user data are stored securely in the session and automatically expire after <strong>10 minutes</strong>.</li>
</ul>
</li>
<li><strong>Interactive & Responsive Dashboard:</strong>
<ul>
<li>A modern, protected dashboard accessible only to authenticated users.</li>
<li>Fetches and displays comprehensive stats in real-time, including:
<ul>
<li>Problems solved (Easy, Medium, Hard)</li>
<li>Languages used (e.g., Python, C++, Java)</li>
<li>Problem-solving skill tags (e.g., Array, Hash Table)</li>
<li>Yearly activity, including total active days and max streak.</li>
</ul>
</li>
</ul>
</li>
<li><strong>Modern Frontend Design:</strong>
<ul>
<li>A visually appealing and fully responsive landing page built with Bootstrap 5.</li>
<li>Enhanced with advanced CSS effects like glassmorphism and floating animations for an engaging user experience.</li>
</ul>
</li>
</ul>

<h2 id="project-structure">🏗️ Project Structure</h2>

<p>The project follows a standard Django layout with three main apps for separation of concerns. Below is a detailed tree view of the directory structure, highlighting key files and their roles:</p>

<pre><code>CodeFolio/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies (Django, Selenium, etc.)
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation (this file)
├── CodeFolio/                  # Main project settings
│   ├── __init__.py
│   ├── asgi.py                 # ASGI config for async support
│   ├── settings.py             # Project configurations (apps, DB, etc.)
│   ├── urls.py                 # Root URL routing
│   └── wsgi.py                 # WSGI config for deployment
├── authentication/             # User auth app
│   ├── static/
│   │   └── authentication/
│   │       └── style.css       # Auth page styles
│   └── templates/
│       └── authentication/
│           ├── sign_in.html    # Login template
│           ├── sign_up.html    # Signup template
│           └── verify.html     # OTP verification template
├── dashboard/                  # User dashboard app
│   ├── static/
│   │   └── dashboard/
│   │       └── style.css       # Dashboard styles
│   └── templates/
│       └── dashboard/
│           └── dashboard.html  # Main dashboard template
└── homepage/                   # Landing page app
│    ├── static/
│    │   └── homepage/
│    │       └── style.css       # Homepage styles
│    └── templates/
         └── homepage/
             └── home.html       # Landing page template
  
</code></pre>

<p><strong>Key Apps Breakdown:</strong></p>
<ul>
<li><strong><code>homepage</code></strong>: Handles the public landing page (<code>views.py</code> renders <code>home.html</code>).</li>
<li><strong><code>authentication</code></strong>: Core auth logic in <code>views.py</code> (signup with OTP, signin, verification via session); forms and templates for UI.</li>
<li><strong><code>dashboard</code></strong>: Protected views in <code>views.py</code> using Selenium/BeautifulSoup for LeetCode scraping; renders stats in <code>dashboard.html</code>.</li>
</ul>

<h2 id="setup-and-installation">🚀 Setup and Installation</h2>

<p>Follow these steps to set up and run the project locally.</p>

<h3>Prerequisites</h3>
<ul>
<li><a href="https://www.python.org/downloads/">Python 3.10+</a></li>
<li><code>pip</code> (Python package installer)</li>
<li><a href="https://www.google.com/chrome/">Google Chrome Browser</a> (for Selenium WebDriver)</li>
</ul>

<h3>Installation Steps</h3>
<ol>
<li><strong>Clone the repository:</strong>
<pre><code>git clone https://www.google.com/search?q=https://github.com/your-username/CodeFolio.git
cd CodeFolio</code></pre>
</li>
<li><strong>Create and activate a virtual environment:</strong>
<pre><code># For Windows
python -m venv venv
.\venv\Scripts\activate

For macOS/Linux
python3 -m venv venv
source venv/bin/activate</code></pre>

</li>
<li><strong>Install dependencies from <code>requirements.txt</code>:</strong>
<pre><code>pip install -r requirements.txt</code></pre>
</li>
<li><strong>Apply database migrations:</strong>
<p>This will create the necessary tables in your database.</p>
<pre><code>python manage.py migrate</code></pre>
</li>
<li><strong>Create a superuser (Optional):</strong>
<p>This allows access to the built-in Django admin interface.</p>
<pre><code>python manage.py createsuperuser</code></pre>
</li>
</ol>

<h2 id="running-the-application">🏃 Running the Application</h2>

<p>Once the setup is complete, you can run the application with a single command.</p>

<pre><code>python manage.py runserver</code></pre>

<p>Your website will be available at <code>http://127.0.0.1:8000/</code>.</p>
<p><strong>Note:</strong> The first time you fetch data for a LeetCode handle, <code>webdriver-manager</code> will automatically download the correct version of ChromeDriver for your installed Chrome browser. This may take a moment.</p>

<h2 id="future-improvements">🔮 Future Improvements</h2>

<ul>
<li><strong>Integrate More Platforms:</strong> Add support for scraping data from other platforms like CodeForces and CodeChef.</li>
<li><strong>Cache Scraped Data:</strong> Implement a caching system (e.g., using Redis) to store scraped results temporarily, reducing load times and avoiding repeated requests.</li>
<li><strong>Data Visualization:</strong> Add charts and graphs to the dashboard to visualize progress and statistics over time.</li>
<li><strong>Public Profile Pages:</strong> Create shareable public profile pages.</li>

