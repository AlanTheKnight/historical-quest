from django.contrib import admin
from imagekit.admin import AdminThumbnail

from .models import Quest, Step, Option, Ending


admin.site.site_header = "Исторические Квесты"
admin.site.site_title = "Исторические Квесты"


class OptionInline(admin.TabularInline):
    model = Option
    extra = 1
    readonly_fields = ("id",)
    fk_name = "step"


class StepInline(admin.TabularInline):
    model = Step
    extra = 1
    readonly_fields = ("id",)


class EndingInline(admin.TabularInline):
    model = Ending
    extra = 1
    readonly_fields = ("id",)


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    inlines = [StepInline]
    list_display = (
        "title",
        "id",
        "description",
        "initial_step",
        "admin_thumbnail",
        "hidden",
        "likes",
    )
    admin_thumbnail = AdminThumbnail(image_field="cover", template="thumbnail.html")
    list_filter = ("hidden",)


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ("title", "id", "quest", "admin_thumbnail")
    admin_thumbnail = AdminThumbnail(image_field="cover", template="thumbnail.html")
    inlines = [OptionInline]
    list_filter = ("quest",)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("text", "id", "step", "admin_thumbnail", "quest", "points")
    admin_thumbnail = AdminThumbnail(image_field="after_cover", template="thumbnail.html")
    list_filter = ("step__quest",)

    def quest(self, obj):
        return obj.step.quest
