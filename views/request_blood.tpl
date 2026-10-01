% rebase("base", title="Request Blood — LifeDrop", user_id=user_id)

<div class="container page"><div class="form-card"><div class="section-heading"><span>REQUEST BLOOD</span><h1>Submit a blood request</h1><p>Provide enough information for the request to be reviewed.</p></div>

% if error:
<div class="alert error">{{error}}</div>

% end

% if success:
<div class="alert success">{{success}}</div>

% end
<form method="post" action="/request-blood" class="form-grid">
<label>Patient Name *<input name="patient_name" required></label>
<label>Required Blood Group *<select name="blood_group" required><option value="">Select</option>
% for g in blood_groups:
<option>{{g}}</option>

% end
</select></label>
<label>Required Units *<input type="number" name="units_required" min="1" required></label>
<label>Hospital Name<input name="hospital_name"></label>
<label class="full">Hospital Address<textarea name="hospital_address" rows="2"></textarea></label>
<label>City<input name="city"></label><label>State<input name="state"></label>
<label>Contact Number<input name="contact_number"></label><label>Required Date<input type="date" name="required_date"></label>
<label>Emergency Level<select name="emergency_level"><option>Normal</option><option>Urgent</option><option>Emergency</option></select></label>
<label class="full">Additional Information<textarea name="additional_information" rows="4"></textarea></label>
<div class="full"><button class="btn primary">Submit Blood Request</button></div>
</form></div></div>

