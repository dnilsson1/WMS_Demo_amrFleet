const API_BASE = "http://localhost:8000";

// Product APIs
// export async function createProduct(product) {
//   const response = await fetch(`${API_BASE}/products/`, {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify(product),
//   });
//   return await response.json();
// }
export async function createProduct(product) {
  try {
    const response = await fetch(`${API_BASE}/products/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(product),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    console.log('REST Body: ', body)
    throw error;
  }
}


export async function getProducts() {
  const response = await fetch(`${API_BASE}/products/`);
  return await response.json();
}

export async function adjustStock(productId, quantity, containerCode = null) {
  const payload = { quantity };
  if (containerCode) {
    payload.container_code = containerCode;
  }
  const response = await fetch(`${API_BASE}/products/${productId}/adjust-stock`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to adjust stock');
  }
  return await response.json();
}

// Container APIs
export async function createContainer(container) {
  const response = await fetch(`${API_BASE}/containers/entry`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(container),
  });
  return await response.json();
}

export async function addProductToContainer(containerCode, productId, quantity) {
  const response = await fetch(`${API_BASE}/containers/${containerCode}/add-product`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_id: productId, quantity }),
  });
  return await response.json();
}

// Order APIs
export async function createOrder(orderData) {
  const response = await fetch(`${API_BASE}/orders/create`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(orderData),
  });
  return await response.json();
}


export async function pickOrder(orderId, destinationName) {
  const response = await fetch(`${API_BASE}/orders/${orderId}/pick`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ destination_name: destinationName }),
  });
  return await response.json();
}

export async function getOrders() {
  const response = await fetch(`${API_BASE}/orders/`);
  return await response.json();
}


// IP Configuration API
export async function setIpConfig(ipConfig) {
  try {
    const response = await fetch(`${API_BASE}/set-ip`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(ipConfig),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

