import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from "react-router-dom";
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { MU_API } from "../../services/auth.service"

const Login = () => {

  const navigate = useNavigate();
  const param = useParams();
  const [id, setId] = useState('');
  const [pw, setPassword] = useState('');

  useEffect(() => {
  }, []);

  const idChangeHandler = (event) => {
    setId(event.target.value);
  };

  const passwordChangeHandler = (event) => {
    setPassword(event.target.value);
  };


  const submitActionHandler = (event) => {
    event.preventDefault();
    MU_API
      .post("app/v1/login", {
        ID: id,
        PW: pw
      })
      .then((response) => {
        console.log(response)
        const user = response.data
        localStorage.setItem("user", JSON.stringify(user));

        alert("MU " + id + " logged in!");

        navigate('/SD')
        window.location.reload();


      }).catch(error => {
        alert("Error Ocurred Login MU:" + error);
      });

  };

  return (
    <Alert variant='primary'>
      <Container>
        <Form onSubmit={submitActionHandler} id="data">
          <Form.Group controlId="form.Name">
            <Form.Label>Id</Form.Label>
            <Form.Control type="text" value={id} onChange={idChangeHandler} placeholder="Enter User Name" required />
          </Form.Group>
          <Form.Group controlId="form.Role">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" value={pw} onChange={passwordChangeHandler} placeholder="Enter Password" required />
          </Form.Group>
          <br></br>
          <Button type='submit'>Login</Button>
          &nbsp;&nbsp;&nbsp;
          <Button type='submit' onClick={() => navigate("/")}>Cancel</Button>
        </Form>
      </Container>
    </Alert>

  );
}
export default Login;