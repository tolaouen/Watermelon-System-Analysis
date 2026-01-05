from flask import Blueprint, redirect, render_template, flash,abort, url_for
from flask_login import login_required
from app.services.permissions import PermissionService
from app.forms.permissions import PermissionCreateForm, PermissionEditForm, PermissionConfirmDelete


permission_router = Blueprint("permissions", __name__, url_prefix="/permissions")

@permission_router.route("/")
@login_required
def index():
    permissions = PermissionService.get_permission_all()
    return render_template("permission/index.html", permissions=permissions)

@permission_router.route("/<int:permission_id>")
@login_required
def detail(permission_id: int):
    permission = PermissionService.get_permission_by_id(permission_id)

    if permission is None:
        abort(404, "User Not Found")

    return render_template("permission/detail.html", permission=permission)

@permission_router.route("/create", methods=["GET", "POST"])
@login_required
def create():

    form = PermissionCreateForm()

    if form.validate_on_submit():
        data = {
            "code": form.code.data,
            "name": form.name.data,
            "module": form.module.data,
            "description": form.description.data,
        }
    
        permission = PermissionService.create_permission(data)

        flash(f"Permission '{permission.code}' was created succesfully.", "success")
        return redirect(url_for('permissions.index'))
    return render_template("permission/create.html", form=form)

@permission_router.route("/<int:permission_id>/edit", methods=["GET", "POST"])
@login_required
def edit(permission_id: int):
    permission = PermissionService.get_permission_by_id(permission_id)

    if permission is None:
        abort(404, "User Not Found")
    
    form = PermissionEditForm(original_permission=permission, obj=permission)

    if form.validate_on_submit():
        data = {
            "code": form.code.data,
            "name": form.name.data,
            "module": form.module.data,
            "description": form.description.data,
        }

        PermissionService.update_permission(permission, data)
        flash(f"Permission '{permission.code}' was updated succesfully.", "succes")
        return redirect(url_for('permissions.detail', permission_id = permission.id))
    
    return render_template("permission/edit.html", form=form, permission=permission)

@permission_router.route("/<int:permission_id>/delete_confirm", methods=["GET"])
@login_required
def delete_confirm(permission_id: int):
    permission = PermissionService.get_permission_by_id(permission_id)

    if permission is None:
        abort(404, "User Not Found")
    
    form = PermissionConfirmDelete()
    return render_template("permission/delete_confirm.html", form=form, permission=permission)

@permission_router.route("/<int:permission_id>/delete", methods=["POST"])
@login_required
def delete(permission_id: int):
    permission = PermissionService.get_permission_by_id(permission_id)

    if permission is None:
        abort(404, "User Not Found")
    
    PermissionService.delete_permission(permission)
    flash("Permis was deleted succesfully.", "success")
    return redirect(url_for('permissions.index'))

