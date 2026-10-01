% rebase("base", title="Admin Inventory — LifeDrop", user_id=user_id)

<div class="container page"><div class="page-head"><div><span>ADMIN</span><h1>Blood Inventory</h1></div><a href="/admin" class="btn light">Back</a></div>
<div class="panel"><h2>Update inventory</h2><form method="post" action="/admin/inventory/update" class="search-bar">
<select name="blood_bank_id" required>
% for b in banks:
<option value="{{b['id']}}">{{b['name']}}</option>

% end
</select>
<select name="blood_group" required>
% for g in blood_groups:
<option>{{g}}</option>

% end
</select>
<input type="number" min="0" name="units" placeholder="Units" required><button class="btn primary">Save</button></form></div>
<div class="panel"><table><thead><tr><th>Bank</th><th>Blood</th><th>Units</th><th>Updated</th></tr></thead><tbody>

% for r in inventory:
<tr><td>{{r["bank_name"]}}</td><td>{{r["blood_group"]}}</td><td>{{r["units"]}}</td><td>{{r["last_updated"]}}</td></tr>

% end
</tbody></table></div></div>

