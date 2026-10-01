% rebase("base", title="Dashboard — LifeDrop", user_id=user_id)

<div class="container page"><div class="page-head"><div><span>MY ACCOUNT</span><h1>Welcome, {{user["full_name"]}}</h1><p>Manage your donor profile and blood requests.</p></div><a class="btn primary" href="/request-blood">Request Blood</a></div>
<div class="dashboard-grid">
<div class="panel"><h2>Donor profile</h2>

% if donor:
<p class="badge success">● {{donor["availability_status"]}}</p><div class="profile-line"><b>Blood group</b><span>{{donor["blood_group"]}}</span></div><div class="profile-line"><b>Location</b><span>{{donor["city"]}}, {{donor["state"]}}</span></div><div class="profile-line"><b>Last donation</b><span>{{donor["last_donation_date"] or "Not provided"}}</span></div><a class="text-link" href="/donor-profile">View profile →</a>


% else:
<p>You have not registered as a donor yet.</p><a class="btn primary" href="/donate">Become a donor</a>


% end
</div>
<div class="panel"><h2>Quick actions</h2><div class="quick-links"><a href="/find-blood">🔎 Find a donor</a><a href="/blood-banks">🏥 Find a blood bank</a><a href="/blood-availability">🩸 Check availability</a><a href="/donation-history">📋 Donation history</a></div></div>
</div>
<div class="panel"><div class="panel-head"><h2>Recent blood requests</h2><a href="/request-blood">+ New request</a></div>

% if requests:
<table><thead><tr><th>Patient</th><th>Blood</th><th>Units</th><th>Emergency</th><th>Status</th></tr></thead><tbody>

% for r in requests:
<tr><td>{{r["patient_name"]}}</td><td>{{r["blood_group"]}}</td><td>{{r["units_required"]}}</td><td>{{r["emergency_level"]}}</td><td><span class="badge">{{r["status"]}}</span></td></tr>


% end
</tbody></table>


% else:
<div class="empty">No blood requests yet.</div>

% end
</div></div>

