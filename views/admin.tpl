% rebase("base", title="Admin Dashboard — LifeDrop", user_id=user_id)

<div class="container page"><div class="page-head"><div><span>ADMIN</span><h1>Management Dashboard</h1><p>Review requests and monitor the demo system.</p></div></div>
<div class="stats admin-stats">

% for label,key in [("Users","users"),("Donors","donors"),("Banks","banks"),("Requests","requests"),("Donations","donations"),("Units","units")]:
<div class="stat"><strong>{{stats[key]}}</strong><span>{{label}}</span></div>


% end
</div>
<div class="admin-links"><a href="/admin/donors">Donors</a><a href="/admin/blood-banks">Blood Banks</a><a href="/admin/inventory">Inventory</a><a href="/admin/requests">Requests</a></div>
<div class="panel"><h2>Recent requests</h2><table><thead><tr><th>Patient</th><th>Group</th><th>Units</th><th>Requester</th><th>Status</th></tr></thead><tbody>

% for r in requests:
<tr><td>{{r["patient_name"]}}</td><td>{{r["blood_group"]}}</td><td>{{r["units_required"]}}</td><td>{{r["requester"] or "—"}}</td><td>{{r["status"]}}</td></tr>

% end
</tbody></table></div>
</div>

