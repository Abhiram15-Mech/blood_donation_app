% rebase("base", title="Admin Requests — LifeDrop", user_id=user_id)

<div class="container page"><div class="page-head"><div><span>ADMIN</span><h1>Blood Requests</h1></div><a href="/admin" class="btn light">Back</a></div>
<div class="panel"><table><thead><tr><th>Patient</th><th>Blood</th><th>Units</th><th>Emergency</th><th>Requester</th><th>Status</th><th>Action</th></tr></thead><tbody>

% for r in requests:
<tr><td>{{r["patient_name"]}}</td><td>{{r["blood_group"]}}</td><td>{{r["units_required"]}}</td><td>{{r["emergency_level"]}}</td><td>{{r["requester"] or "—"}}</td><td>{{r["status"]}}</td><td>
<form method="post" action="/admin/requests/status" class="inline-form"><input type="hidden" name="request_id" value="{{r['id']}}"><select name="status"><option>Pending</option><option>Approved</option><option>Fulfilled</option><option>Rejected</option></select><button>Update</button></form>
</td></tr>


% end
</tbody></table></div></div>

