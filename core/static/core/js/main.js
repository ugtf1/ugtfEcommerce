document.addEventListener("click", async (e) => {
  if (e.target.classList.contains("add-to-cart")) {
    const id = e.target.dataset.id;
    const res = await fetch(`/cart/add/${id}/`, { headers: { "x-requested-with": "XMLHttpRequest" } });
    const data = await res.json();
    const badge = document.getElementById("cartCount");
    if (badge) badge.textContent = data.count;
  }
});