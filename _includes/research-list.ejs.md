<%
const groups = templateParams?.featured
  ? [{items: items.filter(item => item.featured && item["research-type"] === "thesis")}]
  : [
      {title: "Publications", items: items.filter(item => item["research-type"] === "publication")},
      {title: "Working papers", items: items.filter(item => item["research-type"] === "working-paper")},
      {title: "Master's theses", items: items.filter(item => item["research-type"] === "thesis")},
      {title: "Previous research projects", items: items.filter(item => item["research-type"] === "project")}
    ];
for (const group of groups.filter(group => group.items.length)) {
%>
```{=html}
<% if (group.title) { %>
<section class="editorial-section" aria-label="<%- group.title %>">
  <div class="section-label"><h2><%- group.title %></h2></div>
  <div class="section-content">
<% } %>
<ul class="record-list">
  <% for (const item of group.items) { %>
    <li class="research-record">
      <% if (item["record-label"] || item.institution || item.year) { %>
      <p class="record-meta"><%- [item["record-label"], item.institution, item.year].filter(Boolean).join(" · ") %></p>
      <% } %>
      <h3><a href="<%- item.path %>"><%- item.title %></a></h3>
      <% if (!templateParams?.featured && item.award) { %>
      <p class="record-award"><%- item.award %></p>
      <% } %>
      <% if (item.description) { %><p><%- item.description %></p><% } %>
    </li>
  <% } %>
</ul>
<% if (group.title) { %>
  </div>
</section>
<% } %>
```
<% } %>
