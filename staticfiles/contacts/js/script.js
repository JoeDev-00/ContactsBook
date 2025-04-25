// Animations pour les éléments de la page
document.addEventListener("DOMContentLoaded", () => {
  // Animation pour les cartes
  const cards = document.querySelectorAll(".card")
  cards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.1}s`
  })

  // Animation pour les alertes
  const alerts = document.querySelectorAll(".alert")
  alerts.forEach((alert) => {
    // Ajouter une animation de disparition après 5 secondes
    setTimeout(() => {
      if (alert) {
        alert.classList.add("fade")
        setTimeout(() => {
          if (alert.parentNode) {
            alert.parentNode.removeChild(alert)
          }
        }, 500)
      }
    }, 5000)
  })

  // Initialiser les tooltips Bootstrap
  if (typeof bootstrap !== "undefined") {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl))
  }

  // Ajouter une classe active aux liens de navigation correspondant à la page actuelle
  const currentLocation = window.location.pathname
  const navLinks = document.querySelectorAll(".navbar-nav a.nav-link")

  navLinks.forEach((link) => {
    if (link.getAttribute("href") === currentLocation) {
      link.classList.add("active")
    }
  })
})

// Fonction pour copier du texte dans le presse-papier
function copyToClipboard(text) {
  const textarea = document.createElement("textarea")
  textarea.value = text
  document.body.appendChild(textarea)
  textarea.select()
  document.execCommand("copy")
  document.body.removeChild(textarea)

  // Afficher une notification
  showNotification("Copié dans le presse-papier!")
}

// Fonction pour afficher une notification
function showNotification(message, type = "success") {
  const notification = document.createElement("div")
  notification.className = `toast align-items-center text-white bg-${type} border-0`
  notification.setAttribute("role", "alert")
  notification.setAttribute("aria-live", "assertive")
  notification.setAttribute("aria-atomic", "true")

  notification.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `

  const toastContainer = document.createElement("div")
  toastContainer.className = "toast-container position-fixed bottom-0 end-0 p-3"
  toastContainer.appendChild(notification)

  document.body.appendChild(toastContainer)

  if (typeof bootstrap !== "undefined") {
    const toast = new bootstrap.Toast(notification, {
      autohide: true,
      delay: 3000,
    })

    toast.show()
  }

  // Supprimer le conteneur après la disparition
  notification.addEventListener("hidden.bs.toast", () => {
    document.body.removeChild(toastContainer)
  })
}

// Fonction pour confirmer une action
function confirmAction(message) {
  return confirm(message)
}
