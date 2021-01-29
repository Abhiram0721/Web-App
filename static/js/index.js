function pop() {
  document.getElementById("menu_pop").style.zIndex = "10";
  document.getElementById("menu_pop").style.visibility = "visible";
  document.getElementById("menu_pop").style.opacity = "0.9";
  document.getElementById("menu_pop").style.transition = "opacity 0.5s ease";

}



function back() {
  document.getElementById("menu_pop").style.zIndex = "-10";
  document.getElementById("menu_pop").style.visibility = "hidden";
  document.getElementById("menu_pop").style.opacity = "0";
  document.getElementById("menu_pop").style.transition = "opacity 0.5s ease";

}