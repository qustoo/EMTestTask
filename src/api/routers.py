from .controllers.authors import author_router
from .controllers.books import book_router
from .controllers.borrows import borrow_router

routers_v1 = (author_router, book_router, borrow_router)
