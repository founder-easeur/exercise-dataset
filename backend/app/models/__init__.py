"""SQLAlchemy models. Import all model modules so Base.metadata is complete."""
from app.models.anatomy import (  # noqa: F401
    BodyRegion, MuscleGroup, Muscle, Joint, Equipment, ExerciseType,
)
from app.models.exercise import (  # noqa: F401
    Exercise, ExerciseMuscle, ExerciseBodyRegion, ExerciseJoint, ExerciseEquipment,
    ExerciseVariation,
)
from app.models.source import Source, SourceDocument, ExerciseSource  # noqa: F401
from app.models.quality import (  # noqa: F401
    Provenance, DataConflict, ReviewQueueItem, AuditLog, AiEvent, DatasetVersion,
)
from app.models.crawl import CrawlJob, CrawlUrl  # noqa: F401
