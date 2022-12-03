import './App.css';
import "bootstrap/dist/css/bootstrap.min.css";
import { Routes, Route, BrowserRouter, Link, Router } from "react-router-dom";
import React, { useState, useEffect, } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Nav, Navbar, Container } from 'react-bootstrap';

import GenericNotFound from "./components/GenericNotFound"
import AuthService from './services/auth.service';
import EventBus from './common/EventBus';

import Home from "./components/Home.js"

import SD from "./components/SD/SD.js"
import AddSD from "./components/SD/AddSD.js"
import Login from './components/MU/Login';
import Register from './components/MU/Register.js';

function App() {

  const [showConnect, setShowConnect] = useState(true);
  const [currentUser, setCurrentUser] = useState(undefined);

  useEffect(() => {
    const user = AuthService.getCurrentUser();

    console.log(user)

    if (user) {
      setCurrentUser(user);
      setShowConnect(false);
    }

    EventBus.on("logout", () => {
      logOut();
    });

    return () => {
      EventBus.remove("logout");
    };
  }, []);

  const logOut = () => {
    AuthService.MU_API.post("app/v1/logout").then((response) => {
      alert("MU logged out!");
      localStorage.removeItem("user");
      
      window.location.reload();


    }).catch(error => {
      alert("Error Ocurred Logging out MU:" + error);
    });

    setShowConnect(false);
    setCurrentUser(undefined);
  };


  const AppNavbar = () => {
    return (
      <div>
        <Navbar bg="light" variant="light">
          <Container>
            <Navbar.Brand href="#home">IoT</Navbar.Brand>
            <Nav className="me-auto">
              <Nav.Link href="/Home">Home</Nav.Link>
              {showConnect && <Nav.Link href="/MU/Register">Register</Nav.Link>}
              {showConnect && <Nav.Link href="/MU/Login">Login</Nav.Link>}
              {currentUser && <Nav.Link href="/SD/">Profile</Nav.Link>}
              {currentUser && <Nav.Link href="/" onClick={logOut}>Logout</Nav.Link>}


            </Nav>
          </Container>
        </Navbar>

      </div>


      // <div className="card-body" >
      //   <nav className="navbar navbar-expand navbar-dark bg-dark">
      //     <Link to={"/"} className="navbar-brand">
      //       IoT
      //     </Link>
      //     <div className="navbar-nav mr-auto">
      //       <li className="nav-item">
      //         <Link to={"/Home"} className="nav-link">
      //           Home
      //         </Link>
      //       </li>

      //       {showConnect && (
      //         <li className="nav-item">
      //           <Link to={"/MU/Login"} className="nav-link">
      //             Login
      //           </Link>
      //         </li>
      //       )}
      //     </div>




      //     {currentUser ? (
      //       <div className="navbar-nav ml-auto">
      //         <li className="nav-item">
      //           <Link to={"/profile"} className="nav-link">
      //             {currentUser.username}
      //           </Link>
      //         </li>
      //         <li className="nav-item">
      //           <Link to="/MU/Logout" className="nav-link" onClick={logOut}>
      //             LogOut
      //           </Link>
      //         </li>
      //       </div>
      //     ) : (
      //       <div className="navbar-nav ml-auto">
      //         <li className="nav-item">
      //           <Link to={"/MU/Login"} className="nav-link">
      //             Login
      //           </Link>
      //         </li>

      //         <li className="nav-item">
      //           <Link to={"/MU/Register"} className="nav-link">
      //             Register
      //           </Link>
      //         </li>
      //       </div>
      //     )}


      //   </nav>

      // </div>
    )
  }


  return (
    <div className="container card mb-4 box-shadow">

      <div className="card-header">
        <h4 className="my-0 font-weight-normal">IoT - Secure Protocol</h4>
      </div>



      <div>
        <BrowserRouter>
          <AppNavbar />

          <Routes>
            <Route path="/" element={<Home />} />
            <Route exact path={"/Home"} element={<Home />} />

            <Route exact path="/SD" element={<SD />} />
            <Route exact path="/SD/create" element={<AddSD />} />
            <Route exact path="/MU/Login" element={<Login />} />
            <Route exact path="/MU/Register" element={<Register />} />

            <Route path='*' exact={true} element={<GenericNotFound />} />

          </Routes>
        </BrowserRouter>

      </div>

    </div>
  );
}

export default App;
