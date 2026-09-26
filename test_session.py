from app.core.session import SessionManager


session = SessionManager()

session.set("userId", 1)

print("Saved user ID:", session.get("userId"))

session.remove("userId")

print("After removal:", session.get("userId"))

session.set("userId", 2)
session.set("userName", "Layla")

session.clear()

print("After clear:", session.get("userId"))
print("After clear:", session.get("userName"))