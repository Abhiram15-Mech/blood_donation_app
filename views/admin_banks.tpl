% rebase("base", title="Admin Blood Banks — LifeDrop", user_id=user_id)

<div class="container page"><div class="page-head"><div><span>ADMIN</span><h1>Blood Banks</h1></div><a href="/admin" class="btn light">Back</a></div>
<div class="panel"><table><thead><tr><th>Name</th><th>Registration</th><th>City</th><th>Phone</th><th>Email</th></tr></thead><tbody>

% for b in banks:
<tr><td>{{b["name"]}}</td><td>{{b["registration_number"]}}</td><td>{{b["city"]}}</td><td>{{b["phone"]}}</td><td>{{b["email"]}}</td></tr>

% end
</tbody></table></div></div>

