% rebase("base", title="Register — LifeDrop", user_id=user_id)

<div class="container page">
<div class="form-card narrow"><div class="section-heading"><span>ACCOUNT</span><h1>Create your account</h1><p>Register to donate, request blood, and track your activity.</p></div>

% if error:
<div class="alert error">{{error}}</div>

% end
<form method="post" action="/register" class="form-grid">
<label>Full Name *<input name="full_name" required></label>
<label>Email *<input type="email" name="email" required></label>
<label>Phone<input name="phone"></label>
<label>Gender<select name="gender"><option>Prefer not to say</option><option>Male</option><option>Female</option><option>Other</option></select></label>
<label>Date of Birth<input type="date" name="date_of_birth"></label>
<label>City *<input name="city" required></label>
<label>State *<input name="state" required></label>
<label>Password *<input type="password" name="password" minlength="6" required></label>
<label>Confirm Password *<input type="password" name="confirm_password" minlength="6" required></label>
<div class="full"><button class="btn primary" type="submit">Create Account</button></div>
</form><p class="form-foot">Already registered? <a href="/login">Login</a></p></div></div>

