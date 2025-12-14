const updateRowTotals = (row, data) => {
  if (data.total) document.getElementById("cartTotal").textContent = data.total;
  const badge = document.getElementById("cartCount");
  if (badge) badge.textContent = data.count;
};

document.querySelectorAll("#cartBody tr").forEach((row) => {
  const id = row.dataset.id;
  const qtyInput = row.querySelector(".qty-input");
  row.querySelector(".qty-plus").addEventListener("click", async () => {
    qtyInput.value = parseInt(qtyInput.value || "1") + 1;
    const formData = new FormData(); formData.append("qty", qtyInput.value);
    const res = await fetch(`/cart/update/${id}/`, { method: "POST", body: formData, headers: { "X-CSRFToken": getCsrf() }});
    updateRowTotals(row, await res.json());
    // update subtotal locally (optional fetch detailed item totals if you like)
  });
  row.querySelector(".qty-minus").addEventListener("click", async () => {
    qtyInput.value = Math.max(1, parseInt(qtyInput.value || "1") - 1);
    const formData = new FormData(); formData.append("qty", qtyInput.value);
    const res = await fetch(`/cart/update/${id}/`, { method: "POST", body: formData, headers: { "X-CSRFToken": getCsrf() }});
    updateRowTotals(row, await res.json());
  });
  row.querySelector(".remove-item").addEventListener("click", async () => {
    const res = await fetch(`/cart/remove/${id}/`);
    const data = await res.json();
    row.remove();
    updateRowTotals(row, data);
  });
});

function getCsrf() {
  const name = "csrftoken";
  const cookie = document.cookie.split(";").find(c => c.trim().startsWith(name+"="));
  return cookie ? cookie.split("=")[1] : "";
}