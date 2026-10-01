% rebase("base", title="Donor Profile — LifeDrop", user_id=user_id)

<div class="container page"><div class="page-head"><div><span>DONOR PROFILE</span><h1>{{user["full_name"]}}</h1></div><a class="btn primary" href="/donate">Edit profile</a></div>
<div class="profile-card"><div class="avatar">🩸</div><div><h2>{{donor["blood_group"] if donor else "Not registered"}}</h2><p>{{donor["city"] + ", " + donor["state"] if donor else "Register as a donor to create your profile."}}</p></div></div>

% if donor:
<div class="info-grid"><div><b>Availability</b><span>{{donor["availability_status"]}}</span></div><div><b>Email</b><span>{{donor["email"]}}</span></div><div><b>Phone</b><span>{{donor["phone"]}}</span></div><div><b>Last donation</b><span>{{donor["last_donation_date"] or "Not provided"}}</span></div></div>


% end
</div>

