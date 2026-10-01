<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{title or "LifeDrop"}}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
<header class="navbar">
  <div class="container nav-inner">
    <a class="brand" href="/">🩸 <span>LifeDrop</span></a>
    <button class="menu-btn" onclick="toggleMenu()">☰</button>
    <nav id="mainNav">
      <a href="/">Home</a>
      <a href="/find-blood">Find Blood</a>
      <a href="/donate">Donate</a>
      <a href="/blood-banks">Blood Banks</a>
      <a href="/blood-availability">Availability</a>
      
% if user_id:
        <a href="/dashboard">Dashboard</a>
        <a href="/logout">Logout</a>
      

% else:
        <a href="/login">Login</a>
        <a class="nav-cta" href="/register">Register</a>
      

% end
    </nav>
  </div>
</header>
<main>
{{!base}}
</main>
<footer>
  <div class="container footer-grid">
    <div><h3>🩸 LifeDrop</h3><p>Connecting people with blood donors and blood banks.</p></div>
    <div><h4>Explore</h4><a href="/about">About</a><a href="/contact">Contact</a><a href="/blood-availability">Blood Availability</a></div>
    <div><h4>Project</h4><p>Built with Python, Bottle, SQLite3, HTML, CSS and JavaScript.</p></div>
  </div>
  <div class="copyright">© 2026 LifeDrop. Educational project.</div>
</footer>
<script src="/static/js/app.js"></script>
</body>
</html>
