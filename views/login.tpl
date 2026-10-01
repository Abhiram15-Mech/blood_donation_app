% rebase("base", title="Login — LifeDrop", user_id=user_id)

<div class="container page"><div class="form-card narrow">
<div class="section-heading"><span>WELCOME BACK</span><h1>Login</h1><p>Access your LifeDrop dashboard.</p></div>

% if error:
<div class="alert error">{{error}}</div>

% end

% if message:
<div class="alert success">{{message}}</div>

% end
<form method="post" action="/login">
<label>Email<input type="email" name="email" required></label>
<label>Password<input type="password" name="password" required></label>
<button class="btn primary full-btn">Login</button>
</form>
<div class="demo-box"><b>Demo admin</b><br>Email: admin@lifedrop.local<br>Password: admin123</div>
<p class="form-foot">New here? <a href="/register">Create an account</a></p>
</div></div>

