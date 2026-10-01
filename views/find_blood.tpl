% rebase("base", title="Find Donors — LifeDrop", user_id=user_id)

<div class="container page"><div class="section-heading"><span>FIND HELP</span><h1>Find a Blood Donor</h1><p>Search registered donors by blood group and location.</p></div>
<form class="search-bar" method="get" action="/find-donors">
<select name="blood_group"><option value="">All blood groups</option>
% for g in blood_groups:
<option value="{{g}}">{{g}}</option>

% end
</select>
<input name="city" placeholder="City, e.g. Visakhapatnam">
<input name="state" placeholder="State, e.g. Andhra Pradesh">
<button class="btn primary">Search Donors</button>
</form>

% if searched:
<div class="results-head"><h2>Available donors</h2><span>{{len(donors)}} result(s)</span></div>

% if donors:
<div class="cards-grid">
% for d in donors:
<div class="donor-card"><div class="blood-circle">{{d["blood_group"]}}</div><div><h3>{{d["full_name"] or "Registered Donor"}}</h3><p>{{d["city"]}}, {{d["state"]}}</p><span class="badge success">Available</span></div><a href="mailto:{{d['email']}}">Contact</a></div>


% end
</div>


% else:
<div class="empty">No donors found. Try a different blood group or location.</div>

% end


% end
</div>

