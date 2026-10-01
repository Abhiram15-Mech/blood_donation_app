% rebase("base", title="Become a Donor — LifeDrop", user_id=user_id)

<div class="container page"><div class="form-card"><div class="section-heading"><span>DONOR PROGRAM</span><h1>Become a blood donor</h1><p>Keep your availability information current so people can find help.</p></div>

% if error:
<div class="alert error">{{error}}</div>

% end
<form method="post" action="/donate" class="form-grid">
<label>Blood Group *<select name="blood_group" required><option value="">Select</option>
% for g in blood_groups:
<option value="{{g}}">{{g}}</option>

% end
</select></label>
<label>Gender<select name="gender"><option>Prefer not to say</option><option>Male</option><option>Female</option><option>Other</option></select></label>
<label>Date of Birth<input type="date" name="date_of_birth" value="{{user['date_of_birth'] or ''}}"></label>
<label>Phone<input name="phone" value="{{user['phone'] or ''}}"></label>
<label>Email<input type="email" name="email" value="{{user['email']}}"></label>
<label>City<input name="city" value="{{user['city'] or ''}}"></label>
<label>State<input name="state" value="{{user['state'] or ''}}"></label>
<label>Last Donation Date<input type="date" name="last_donation_date"></label>
<label>Availability<select name="availability_status"><option>Available</option><option>Not Available</option></select></label>
<label class="full">Address<textarea name="address" rows="3"></textarea></label>
<div class="full"><button class="btn primary">Save Donor Profile</button></div>
</form></div></div>

