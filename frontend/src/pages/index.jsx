// import React, { useEffect, useState } from "react";
// import "./Home.css";

// const Home = () => {
//   const [slideIndex, setSlideIndex] = useState(0);

//   const images = [
//     "/static/image1.jpeg",
//     "/static/image2.jpeg",
//     "/static/image3.webp",
//   ];

//   useEffect(() => {
//     const interval = setInterval(() => {
//       setSlideIndex((prev) => (prev + 1) % images.length);
//     }, 3000);
//     return () => clearInterval(interval);
//   }, []);

//   const nextSlide = (n) => {
//     setSlideIndex((prev) => (prev + n + images.length) % images.length);
//   };

//   return (
//     <div>
//       <nav>
//         <ul>
//           <li><a href="/">🏠 Home</a></li>
//           <li>
//             <a href="/">👤 Owners</a>
//             <ul>
//               <li><a href="/add_owner">Add Owner</a></li>
//               <li><a href="/modify_owner">Edit Owner</a></li>
//               <li><a href="/delete_owner">Delete Owner</a></li>
//               <li><a href="/list_owners">List Owners</a></li>
//             </ul>
//           </li>
//           <li style={{ marginLeft: "auto" }}>
//       <button
//         onClick={() => {
//           localStorage.removeItem("token"); // Or sessionStorage.clear()
//           window.location.href = "/login";  // Redirect to login
//         }}
//         style={{
//           backgroundColor: "#39e66aff",
//           color: "white",
//           padding: "8px 16px",
//           border: "none",
//           borderRadius: "5px",
//           cursor: "pointer"
//         }}
//       >
//          Logout
//       </button>
//     </li>
//           {/* ... rest of navbar ... */}
//         </ul>
//       </nav>

//       <div style={{ padding: "20px" }}>
//         <h2 style={{ textAlign: "center" }}>Welcome to Property Management App</h2>
//       </div>

//       <div className="slideshow-container">
//         {images.map((img, i) => (
//           <div
//             className="slide"
//             style={{ display: slideIndex === i ? "block" : "none" }}
//             key={i}
//           >
//             <img src={img} alt={`Slide ${i + 1}`} />
//           </div>
//         ))}
// <button className="prev" onClick={() => nextSlide(-1)} aria-label="Previous Slide">
//   &#10094;
// </button>
// <button className="next" onClick={() => nextSlide(1)} aria-label="Next Slide">
//   &#10095;
// </button>
//       </div>
//     </div>
//   );
// };

// export default Home;
