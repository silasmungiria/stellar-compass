import React, { useState, useEffect } from "react";
import { Form, Row, Col, Button, Alert } from "react-bootstrap";
import { useForm } from "react-hook-form";
import { useFlutterwave, closePaymentModal } from "flutterwave-react-v3";

const CreateNewOrder = ({ show }) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm();
  const [medicines, setMedicines] = useState([]);
  const [users, setUsers] = useState([]);
  const [serverResponse, setServerResponse] = useState(null);
  const [orderData, setOrderData] = useState(null);

  const config = {
    public_key: "FLWPUBK-**************************-X",
    tx_ref: Date.now(),
    amount: 100,
    currency: "NGN",
    payment_options: "card,mobilemoney,ussd",
    customer: {
      email: "user@gmail.com",
      phone_number: "070********",
      name: "john doe",
    },
    customizations: {
      title: "my Payment Title",
      description: "Payment for items in submitForm",
      logo: "https://st2.depositphotos.com/4403291/7418/v/450/depositphotos_74189661-stock-illustration-online-shop-log.jpg",
    },
  };

  const handleFlutterPayment = useFlutterwave(config);

  useEffect(() => {
    fetchMedicines();
    fetchUsers();
  }, []);

  const fetchMedicines = async () => {
    try {
      const response = await fetch("/medicines/medications");
      const data = await response.json();
      setMedicines(data);
    } catch (error) {
      console.error("Error fetching medicines:", error);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await fetch("/users/users");
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };

  const submitForm = async (data) => {
    try {
      const token = localStorage.getItem("REACT_TOKEN_AUTH_KEY");
      const orderType = data.order_type === "Shipping";

      const body = {
        user_id: parseInt(data.user_id),
        medication_id: parseInt(data.medication_id),
        quantity: parseInt(data.quantity),
        order_type: orderType,
      };

      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${JSON.parse(token)}`,
        },
        body: JSON.stringify(body),
      };

      const response = await fetch("/orders/orders", requestOptions);
      const responseData = await response.json();

      if (response.ok) {
        reset();
        window.location.reload();
      }

      setServerResponse(responseData.message);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handlePayNow = async (data) => {
    try {
      setOrderData(data); // Store order data in state

      handleFlutterPayment({
        callback: async (response) => {
          console.log(response);
          closePaymentModal(); // Close the modal programmatically

          if (response.status === "successful") {
            await submitForm(orderData); // Submit the form if payment successful
          } else {
            alert("Payment was unsuccessful");
            window.location.href = "/orders"; // Redirect if payment unsuccessful
          }
        },
        onClose: () => {
          // Handle modal closure if needed
        },
      });
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div style={{ display: show ? "block" : "none" }}>
      {serverResponse && (
        <Alert
          variant={
            serverResponse.includes("successfully") ? "success" : "danger"
          }
        >
          {serverResponse}
        </Alert>
      )}

      <Form onSubmit={handleSubmit(submitForm)}>
        <Row>
          <Col md={6} className="mb-3">
            <Form.Group>
              <Form.Label>User</Form.Label>
              <Form.Select {...register("user_id", { required: true })}>
                <option value="">Select User</option>
                {users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.username}
                  </option>
                ))}
              </Form.Select>
              {errors.user_id && (
                <p className="text-danger small">User is required</p>
              )}
            </Form.Group>
          </Col>

          <Col md={6} className="mb-3">
            <Form.Group>
              <Form.Label>Medicine</Form.Label>
              <Form.Select {...register("medication_id", { required: true })}>
                <option value="">Select Medicine</option>
                {medicines.map((medicine) => (
                  <option key={medicine.id} value={medicine.id}>
                    {medicine.name}
                  </option>
                ))}
              </Form.Select>
              {errors.medication_id && (
                <p className="text-danger small">Medicine is required</p>
              )}
            </Form.Group>
          </Col>

          <Col md={6} className="mb-3">
            <Form.Group>
              <Form.Label>Quantity</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter Quantity"
                {...register("quantity", { required: true })}
              />
              {errors.quantity && (
                <p className="text-danger small">Quantity is required</p>
              )}
            </Form.Group>
          </Col>

          <Col md={6} className="mb-3">
            <Form.Group>
              <Form.Label>Order Type</Form.Label>
              <Form.Select {...register("order_type", { required: true })}>
                <option value="">Select Order Type</option>
                <option value="Shipping">Shipping</option>
                <option value="Pickup">Pickup</option>
              </Form.Select>
              {errors.order_type && (
                <p className="text-danger small">Order Type is required</p>
              )}
            </Form.Group>
          </Col>
        </Row>

        <Row className="justify-content-around">
          <Col xs={6} md={4} className="mb-3">
            <Button
              variant="primary"
              block
              className="w-100"
              onClick={handleSubmit(handlePayNow)}
            >
              Pay Now
            </Button>
          </Col>
          <Col xs={6} md={4}>
            <Button variant="success" type="submit" block className="w-100">
              Pay Later
            </Button>
          </Col>
        </Row>
      </Form>
    </div>
  );
};

export default CreateNewOrder;
