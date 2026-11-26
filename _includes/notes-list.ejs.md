<% if (items.length) { %>
```{=html}
<section class="notes-archive">
  <h2>Published notes</h2>
  <ul class="list notes-records">
  <% for (const item of items) { %>
    <li class="compact-record note-record" <%= metadataAttrs(item) %>>
      <p class="listing-date record-date"><%- item.date %></p>
      <div>
        <h3><a class="listing-title" href="<%- item.path %>"><%- item.title %></a></h3>
        <% if (item.categories?.length) { %>
        <p class="listing-categories record-meta"><%- item.categories.join(" · ") %></p>
        <% } %>
      </div>
    </li>
  <% } %>
  </ul>
</section>
```
<% } %>
