<% if (items.length) { %>
```{=html}
<% if (templateParams?.heading) { %>
<section class="editorial-section" aria-label="<%- templateParams.heading %>">
  <div class="section-label"><h2><%- templateParams.heading %></h2></div>
  <div class="section-content">
<% } %>
<ul class="record-list">
  <% for (const item of items) { %>
    <li class="research-record">
      <% if (item["record-label"] || item.period) { %>
      <p class="record-meta"><%- [item["record-label"], item.period].filter(Boolean).join(" · ") %></p>
      <% } %>
      <h3><a href="<%- item.path %>"><%- item.title %></a></h3>
      <% if (item.description) { %><p><%- item.description %></p><% } %>
    </li>
  <% } %>
</ul>
<% if (templateParams?.heading) { %>
  </div>
</section>
<% } %>
```
<% } %>
