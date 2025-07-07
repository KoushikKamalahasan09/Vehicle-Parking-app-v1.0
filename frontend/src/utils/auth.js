export function requireAdminAccess(router) {
  const isAdmin = localStorage.getItem('isadmin')

  if (!isAdmin || isAdmin === 'false') {
    router.push('/dashboard')
  }
}

export function requireNonAdminAccess(router) {
  const isAdmin = localStorage.getItem('isadmin')
  if (isAdmin === 'true') {
    router.push('/admin/dashboard')
  }
}