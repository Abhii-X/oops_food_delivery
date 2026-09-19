import { useState } from "react"
import "./App.css"

function App() {

  const [restaurants, setRestaurants] = useState([])
  const [foods, setFoods] = useState([])
  const [cart, setCart] = useState([])

  const [showRestaurants, setShowRestaurants] = useState(false)
  const [showCart, setShowCart] = useState(false)
  const [showOrders, setShowOrders] = useState(false)

  const [selectedRestaurant, setSelectedRestaurant] = useState(null)

  const [order, setOrder] = useState(null)
  const [payment, setPayment] = useState(null)
  const [delivery, setDelivery] = useState(null)

  const [orders, setOrders] = useState([])
  const [selectedOrder, setSelectedOrder] = useState(null)

  const [message, setMessage] = useState("")


  async function getRestaurants() {

    const response = await fetch(
      "http://127.0.0.1:8000/restaurants/"
    )

    const data = await response.json()

    setRestaurants(data)
    setShowRestaurants(true)
    setShowOrders(false)
    setShowCart(false)
  }


  async function getFoods(restaurantId) {

    const response = await fetch(
      `http://127.0.0.1:8000/foods/restaurant/${restaurantId}`
    )

    const data = await response.json()

    setFoods(data)
    setSelectedRestaurant(restaurantId)
    setShowCart(false)
  }


  function addToCart(food) {

    setCart((currentCart) => {

      const existingItem = currentCart.find(
        (item) => item.food.id === food.id
      )

      if (existingItem) {

        return currentCart.map((item) => {

          if (item.food.id === food.id) {

            return {
              ...item,
              quantity: item.quantity + 1
            }
          }

          return item
        })
      }

      return [
        ...currentCart,
        {
          food: food,
          quantity: 1
        }
      ]
    })

    setMessage(`${food.name} added to cart`)
  }


  function increaseQuantity(foodId) {

    setCart((currentCart) => {

      return currentCart.map((item) => {

        if (item.food.id === foodId) {

          return {
            ...item,
            quantity: item.quantity + 1
          }
        }

        return item
      })
    })
  }


  function decreaseQuantity(foodId) {

    setCart((currentCart) => {

      return currentCart
        .map((item) => {

          if (item.food.id === foodId) {

            return {
              ...item,
              quantity: item.quantity - 1
            }
          }

          return item
        })
        .filter((item) => item.quantity > 0)
    })
  }


  function removeFromCart(foodId) {

    setCart((currentCart) => {

      return currentCart.filter(
        (item) => item.food.id !== foodId
      )
    })
  }


  function calculateTotal() {

    let total = 0

    for (let item of cart) {

      total += item.food.price * item.quantity
    }

    return total
  }


  function calculateCartItems() {

    let count = 0

    for (let item of cart) {

      count += item.quantity
    }

    return count
  }


  function openCart() {

    setShowCart(true)
    setShowRestaurants(false)
    setShowOrders(false)
  }


  async function placeOrder() {

    const items = cart.map((item) => {

      return {
        food_id: item.food.id,
        quantity: item.quantity
      }
    })

    const response = await fetch(
      "http://127.0.0.1:8000/orders/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          customer_id: 1,
          items: items
        })
      }
    )

    const data = await response.json()

    if (!response.ok) {

      setMessage(data.detail)
      return
    }

    setOrder(data)
    setCart([])
    setPayment(null)
    setDelivery(null)
    setSelectedOrder(null)

    setShowCart(false)

    setMessage("Order placed successfully")
  }


  async function makePayment(method) {

    const response = await fetch(
      "http://127.0.0.1:8000/payments/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          order_id: order.order_id,
          method: method
        })
      }
    )

    const data = await response.json()

    if (!response.ok) {

      setMessage(data.detail)
      return
    }

    setPayment(data)

    setMessage("Payment successful")
  }


  async function createDelivery() {

    const response = await fetch(
      "http://127.0.0.1:8000/deliveries/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          order_id: order.order_id
        })
      }
    )

    const data = await response.json()

    if (!response.ok) {

      setMessage(data.detail)
      return
    }

    setDelivery(data)

    setMessage("Delivery assigned successfully")
  }


  async function getOrders() {

    const response = await fetch(
      "http://127.0.0.1:8000/orders/"
    )

    const data = await response.json()

    setOrders(data)

    setShowOrders(true)
    setShowRestaurants(false)
    setShowCart(false)
  }


  async function getOrderDetails(orderId) {

    const response = await fetch(
      `http://127.0.0.1:8000/orders/${orderId}`
    )

    const data = await response.json()

    if (!response.ok) {

      setMessage(data.detail)
      return
    }

    setSelectedOrder(data)
  }


  return (
    <div className="app">

      <header>

        <div className="header-content">

          <div>

            <h1>Food Delivery</h1>

            <p>
              Fresh food delivered to your doorstep
            </p>

          </div>

          <div className="header-buttons">

            <button onClick={getRestaurants}>
              Restaurants
            </button>

            <button onClick={openCart}>
              Cart ({calculateCartItems()})
            </button>

            <button onClick={getOrders}>
              My Orders
            </button>

          </div>

        </div>

      </header>


      <main>

        <section className="hero">

          <h2>
            Order your favourite food
          </h2>

          <p>
            Choose a restaurant, select your food,
            place your order and track your delivery.
          </p>

          <button
            className="hero-button"
            onClick={getRestaurants}
          >
            Start Ordering
          </button>

        </section>


        {message && (

          <section className="message-section">

            <p>
              {message}
            </p>

          </section>

        )}


        {showRestaurants && (

          <section className="section">

            <h2>
              Restaurants
            </h2>

            <div className="restaurant-list">

              {restaurants.map((restaurant) => (

                <div
                  className="restaurant-card"
                  key={restaurant.id}
                >

                  <div className="restaurant-icon">
                    🍴
                  </div>

                  <h3>
                    {restaurant.name}
                  </h3>

                  <p>
                    {restaurant.address}
                  </p>

                  <button
                    onClick={() =>
                      getFoods(restaurant.id)
                    }
                  >
                    View Menu
                  </button>

                </div>

              ))}

            </div>

          </section>

        )}


        {selectedRestaurant && (

          <section className="section">

            <h2>
              Food Menu
            </h2>

            <div className="food-list">

              {foods.map((food) => (

                <div
                  className="food-card"
                  key={food.id}
                >

                  <div className="food-icon">
                    🍽️
                  </div>

                  <h3>
                    {food.name}
                  </h3>

                  <p className="category">
                    {food.category}
                  </p>

                  <h3>
                    ₹{food.price}
                  </h3>

                  <button
                    onClick={() =>
                      addToCart(food)
                    }
                  >
                    Add to Cart
                  </button>

                </div>

              ))}

            </div>

          </section>

        )}


        {showCart && (

          <section className="section cart-section">

            <h2>
              My Cart
            </h2>

            {cart.length === 0 ? (

              <div className="empty-box">

                <h3>
                  Your cart is empty
                </h3>

                <p>
                  Add some delicious food to continue.
                </p>

                <button onClick={getRestaurants}>
                  Browse Restaurants
                </button>

              </div>

            ) : (

              <>

                <div className="cart-list">

                  {cart.map((item) => (

                    <div
                      className="cart-item"
                      key={item.food.id}
                    >

                      <div className="cart-info">

                        <h3>
                          {item.food.name}
                        </h3>

                        <p>
                          ₹{item.food.price} each
                        </p>

                      </div>


                      <div className="quantity">

                        <button
                          onClick={() =>
                            decreaseQuantity(item.food.id)
                          }
                        >
                          -
                        </button>

                        <span>
                          {item.quantity}
                        </span>

                        <button
                          onClick={() =>
                            increaseQuantity(item.food.id)
                          }
                        >
                          +
                        </button>

                      </div>


                      <div className="item-total">

                        ₹{item.food.price * item.quantity}

                      </div>


                      <button
                        className="remove-button"
                        onClick={() =>
                          removeFromCart(item.food.id)
                        }
                      >
                        Remove
                      </button>

                    </div>

                  ))}

                </div>


                <div className="cart-summary">

                  <h3>
                    Total: ₹{calculateTotal()}
                  </h3>

                  <button
                    className="order-button"
                    onClick={placeOrder}
                  >
                    Place Order
                  </button>

                </div>

              </>

            )}

          </section>

        )}


        {order && (

          <section className="section order-section">

            <div className="order-card">

              <div className="success-icon">
                ✓
              </div>

              <h2>
                Order Confirmed
              </h2>

              <p>
                Your order has been placed successfully.
              </p>

              <div className="order-details">

                <div>
                  <span>Order ID</span>
                  <strong>#{order.order_id}</strong>
                </div>

                <div>
                  <span>Total</span>
                  <strong>₹{order.total}</strong>
                </div>

                <div>
                  <span>Status</span>
                  <strong>{order.status}</strong>
                </div>

              </div>


              {!payment && (

                <div className="payment-box">

                  <h3>
                    Choose Payment Method
                  </h3>

                  <button
                    onClick={() =>
                      makePayment("UPI")
                    }
                  >
                    UPI
                  </button>

                  <button
                    onClick={() =>
                      makePayment("CARD")
                    }
                  >
                    Card
                  </button>

                  <button
                    onClick={() =>
                      makePayment("COD")
                    }
                  >
                    Cash on Delivery
                  </button>

                </div>

              )}


              {payment && (

                <div className="payment-success">

                  <h3>
                    Payment Successful
                  </h3>

                  <p>
                    Payment ID: {payment.payment_id}
                  </p>

                  <p>
                    Method: {payment.method}
                  </p>

                  <p>
                    Amount: ₹{payment.amount}
                  </p>

                  <p>
                    Status: {payment.status}
                  </p>


                  {!delivery && (

                    <button
                      className="delivery-button"
                      onClick={createDelivery}
                    >
                      Track Delivery
                    </button>

                  )}

                </div>

              )}


              {delivery && (

                <div className="delivery-success">

                  <div className="delivery-icon">
                    🚚
                  </div>

                  <h3>
                    Delivery Assigned
                  </h3>

                  <p>
                    Delivery ID: #{delivery.delivery_id}
                  </p>

                  <p>
                    Address: {delivery.address}
                  </p>

                  <p>
                    Status: {delivery.status}
                  </p>

                </div>

              )}

            </div>

          </section>

        )}


        {showOrders && (

          <section className="section orders-section">

            <h2>
              My Orders
            </h2>

            {orders.length === 0 ? (

              <div className="empty-box">

                <h3>
                  No orders found
                </h3>

                <p>
                  You haven't placed any orders yet.
                </p>

              </div>

            ) : (

              <div className="orders-list">

                {orders.map((item) => (

                  <div
                    className="previous-order"
                    key={item.order_id}
                  >

                    <div>

                      <h3>
                        Order #{item.order_id}
                      </h3>

                      <p>
                        Customer ID: {item.customer_id}
                      </p>

                    </div>

                    <div>

                      <span className="status">
                        {item.status}
                      </span>

                      <button
                        onClick={() =>
                          getOrderDetails(item.order_id)
                        }
                      >
                        View Details
                      </button>

                    </div>

                  </div>

                ))}

              </div>

            )}


            {selectedOrder && (

              <div className="selected-order">

                <h2>
                  Order #{selectedOrder.order_id}
                </h2>

                <p>
                  Customer: {selectedOrder.customer_email}
                </p>

                <p>
                  Status: {selectedOrder.status}
                </p>

                <div className="selected-items">

                  {selectedOrder.items.map((item) => (

                    <div
                      className="selected-item"
                      key={item.food_id}
                    >

                      <div>

                        <strong>
                          {item.food_name}
                        </strong>

                        <p>
                          ₹{item.price} × {item.quantity}
                        </p>

                      </div>

                      <strong>
                        ₹{item.item_total}
                      </strong>

                    </div>

                  ))}

                </div>

                <h3 className="selected-total">
                  Total: ₹{selectedOrder.total}
                </h3>

              </div>

            )}

          </section>

        )}

      </main>


      

    </div>
  )
}

export default App