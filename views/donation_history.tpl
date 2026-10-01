% rebase("base", title="Donation History — LifeDrop", user_id=user_id)

<div class="container page"><div class="section-heading"><span>MY ACTIVITY</span><h1>Donation History</h1><p>Your recorded blood donations.</p></div>
<div class="panel">

% if donations:
<table><thead><tr><th>Date</th><th>Blood Group</th><th>Blood Bank</th><th>Units</th><th>Status</th></tr></thead><tbody>

% for d in donations:
<tr><td>{{d["donation_date"]}}</td><td>{{d["blood_group"]}}</td><td>{{d["bank_name"]}}</td><td>{{d["units_donated"]}}</td><td><span class="badge success">{{d["status"]}}</span></td></tr>

% end
</tbody></table>


% else:
<div class="empty">No donation records yet.</div>

% end
</div></div>

