% rebase("base", title="LifeDrop — Blood Donation & Blood Bank Management", user_id=user_id)

<section class="hero">
  <div class="container hero-grid">
    <div>
      <span class="eyebrow">BLOOD DONATION • COMMUNITY • HOPE</span>
      <h1>Every drop of blood can <span>save a life.</span></h1>
      <p>Find blood, become a donor, discover nearby blood banks, and help people when they need it most.</p>
      <div class="actions"><a class="btn primary" href="/find-blood">Find a Donor</a><a class="btn light" href="/donate">Become a Donor</a></div>
    </div>
    <div class="hero-card">
      <div class="drop">🩸</div><h3>Be someone's hope today.</h3><p>A simple local platform for learning and managing blood donation information.</p>
    </div>
  </div>
</section>
<section class="container stats">
  <div class="stat"><strong>{{stats["donors"]}}</strong><span>Registered Donors</span></div>
  <div class="stat"><strong>{{stats["banks"]}}</strong><span>Blood Banks</span></div>
  <div class="stat"><strong>{{stats["units"]}}</strong><span>Blood Units</span></div>
  <div class="stat"><strong>{{stats["donations"]}}</strong><span>Completed Donations</span></div>
</section>
<section class="section container">
  <div class="section-heading"><span>KNOW YOUR TYPES</span><h2>Blood groups</h2><p>Blood inventory is organized by the eight common ABO/Rh groups.</p></div>
  <div class="blood-grid">
    
% for group in blood_groups:
      <a class="blood-card" href="/blood-banks?blood_group={{group}}"><b>{{group}}</b><span>View availability →</span></a>
    

% end
  </div>
</section>
<section class="section soft">
 <div class="container">
  <div class="section-heading"><span>HOW IT WORKS</span><h2>Three simple steps</h2></div>
  <div class="steps">
    <div class="step"><b>01</b><h3>Register</h3><p>Create an account and tell us whether you want to donate or request blood.</p></div>
    <div class="step"><b>02</b><h3>Connect</h3><p>Search donors, blood banks, inventory, or submit a blood request.</p></div>
    <div class="step"><b>03</b><h3>Help</h3><p>Coordinate with the appropriate donor or blood bank.</p></div>
  </div>
 </div>
</section>
<section class="container callout"><div><h2>Ready to help?</h2><p>Register as a donor and make your availability visible to the community.</p></div><a class="btn primary" href="/register">Create account</a></section>

