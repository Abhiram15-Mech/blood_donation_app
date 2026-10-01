% rebase("base", title="Blood Banks — LifeDrop", user_id=user_id)

<div class="container page"><div class="section-heading"><span>FIND BLOOD BANKS</span><h1>Blood Banks</h1><p>Search blood banks and see inventory totals.</p></div>
<form class="search-bar" method="get" action="/blood-banks">
<select name="blood_group"><option value="">Any blood group</option>
% for g in blood_groups:
<option value="{{g}}" {{'selected' if selected_group==g else ''}}>{{g}}</option>

% end
</select>
<input name="city" placeholder="City"><input name="state" placeholder="State"><button class="btn primary">Search</button>
</form>
<div class="cards-grid">

% for b in banks:
<div class="bank-card"><div class="bank-icon">🏥</div><div><h3>{{b["name"]}}</h3><p>{{b["address"]}}, {{b["city"]}}, {{b["state"]}}</p><p>☎ {{b["phone"]}}</p><span class="badge">{{(str(b["requested_group_units"]) + " units of " + selected_group) if selected_group else str(b["total_units"]) + " total units"}}</span></div></div>


% end
</div>

% if not banks:
<div class="empty">No blood banks found.</div>

% end
</div>

