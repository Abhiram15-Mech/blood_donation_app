% rebase("base", title="Blood Availability — LifeDrop", user_id=user_id)

<div class="container page"><div class="section-heading"><span>LIVE INVENTORY</span><h1>Blood Availability</h1><p>Totals are calculated from the SQLite blood inventory.</p></div>
<div class="availability-grid">

% for g in blood_groups:
  <% units = availability.get(g, 0) %>
  <div class="availability-card"><div class="blood-circle">{{g}}</div><div><h3>{{units}} units</h3><p class="{{'stock-good' if units>=5 else 'stock-low' if units>0 else 'stock-none'}}">{{'Available' if units>=5 else 'Low Stock' if units>0 else 'Not Available'}}</p></div></div>


% end
</div>
<div class="note">Inventory shown here is sample data for this educational project. Real blood availability must be confirmed directly with an authorized blood bank.</div>
</div>

