import pytest


@pytest.fixture
def sra_output_folder():
    return "s3://olgabot-maca/sra/danio_rerio/" \
           "smart-seq/whole_kidney_marrow_prjna393431/"


def test_get_fastqs_as_r1_r2_columns(sra_output_folder):
    from aguamenti.s3_utils import get_fastqs_as_r1_r2_columns
    fastqs = get_fastqs_as_r1_r2_columns(s3_input_path=sra_output_folder)

    # 246 samples --> 492 reads
    assert len(fastqs) == 246
