from flask import url_for, render_template, redirect, flash, abort, Blueprint
from flask_login import login_required
from app.services.users import UserService
from app.forms.users import UserCreateForm, UserEditForm, ConfirmDeleteForm


user_router = Blueprint("users", __name__, url_prefix="/users")


@user_router.route("/")
@login_required
def index():
    users = UserService.get_user_all()
    return render_template("users/index.html", users=users)


@user_router.route("/<int:user_id>")
@login_required
def detail(user_id: int):
    user = UserService.get_user_by_id(user_id)
    if user is None:
        abort(404, "User Not Found")
    return render_template("users/detail.html", user=user)


@user_router.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = UserCreateForm()

    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "is_active": form.is_active.data if hasattr(form, "is_active") else True,
        }
        password = form.password.data
        role_id = form.role_id.data or None
        user = UserService.create_user(data, password, role_id)
        flash(f"User '{user.username}' was created successfully.", "success")
        return redirect(url_for("users.detail", user_id=user.id))
    return render_template("users/create.html", form=form)


@user_router.route("/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def edit(user_id: int):
    user = UserService.get_user_by_id(user_id)
    if user is None:
        abort(404, "User not found")

    form = UserEditForm(original_user=user, obj=user)

    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "email": form.email.data,
            "full_name": form.full_name.data,
            "is_active": form.is_active.data if hasattr(form, "is_active") else True,
        }
        password = form.password.data or None
        role_id = form.role_id.data or None
        UserService.update_user(user, data, password, role_id)
        flash(f"User '{user.username}' was updated successfully.", "success")
        return redirect(url_for("users.detail", user_id=user.id))

    return render_template("users/edit.html", form=form, user=user)


@user_router.route("/<int:user_id>/delete", methods=["GET"])
@login_required
def delete_confirm(user_id: int):
    user = UserService.get_user_by_id(user_id)
    if user is None:
        abort(404, "User not found")

    form = ConfirmDeleteForm()
    return render_template("users/delete_confirm.html", user=user, form=form)


@user_router.route("/<int:user_id>/delete", methods=["POST"])
@login_required
def delete(user_id: int):
    user = UserService.get_user_by_id(user_id)
    if user is None:
        abort(404, "User not found")

    UserService.delete_user(user)
    flash("User was deleted successfully", "success")
    return redirect(url_for("users.index"))