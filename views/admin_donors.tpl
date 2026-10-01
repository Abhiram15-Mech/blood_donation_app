% rebase("base", title="Admin Donors — LifeDrop", user_id=user_id)

<div class="container page"><div class="page-head"><div><span>ADMIN</span><h1>Donors</h1></div><a href="/admin" class="btn light">Back</a></div>
<div class="panel"><table><thead><tr><th>Name</th><th>Blood</th><th>City</th><th>State</th><th>Availability</th><th>Contact</th></tr></thead><tbody>

% for d in donors:
<tr><td>{{d["full_name"]}}</td><td>{{d["blood_group"]}}</td><td>{{d["city"]}}</td><td>{{d["state"]}}</td><td>{{d["availability_status"]}}</td><td>{{d["email"]}}</td></tr>

% end
</tbody></table></div></div>

