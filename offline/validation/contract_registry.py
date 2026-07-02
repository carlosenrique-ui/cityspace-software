from __future__ import annotations
from pathlib import Path
from typing import Dict, Any


def build_contract(base_dir: Path) -> Dict[str, Any]:
    engine_root = base_dir.resolve()

    return {
        "meta": {
            "system_name": "IPT-CitySpace",
            "version": "3.1-expanded-safe",
            "contract_mode": "evolutionary",
            "critical_system": True,
            "development_environment": {
                "platform": "WSL Ubuntu",
                "python_env": "geo_env_2018",
                "toolchain": [
                    "Python",
                    "Rasterio",
                    "GDAL",
                    "Shapely",
                    "NumPy",
                    "Pandas",
                    "GeoPandas",
                ],
                "purpose": "scientific_geospatial_software_and_commercial_python",
            },
        },
        "paths": {
            "scientific_grid_csv": "/mnt/c/workspace/ipt-cityspace-engine/ipt_core_clean/offline/products/scientific/grid_metrics_utm.csv",
            "official_products_dir": "/mnt/c/workspace/ipt-cityspace-engine/ipt_core_clean/offline/products",
            "official_runtime_dir": "/mnt/c/workspace/ipt-cityspace-engine/ipt_core_clean/offline/products/runtime",
            "report_dir": "/mnt/c/workspace/ipt-cityspace-engine/ipt_core_clean/offline/validation/reports",
            "legacy_forbidden_as_official_source": [
                "products/final/grid_height.csv",
            ],
        },
        "reference_systems": {
            "mandatory": [
                {
                    "id": "SR-1",
                    "name": "utm",
                    "description": "Sistema geoespacial territorial real.",
                },
                {
                    "id": "SR-2",
                    "name": "cartesian_trigonometric",
                    "description": "Sistema intermedi\u00e1rio para rota\u00e7\u00f5es, transla\u00e7\u00f5es, PCA e alinhamentos.",
                },
                {
                    "id": "SR-3",
                    "name": "physical_table",
                    "description": "Sistema final da mesa tang\u00edvel.",
                },
            ],
            "transformation_chain": [
                "UTM -> Cartesian Trigonometric -> Physical Table",
            ],
        },
        "data_schema": {
            "base_scientific_columns": [
                "row",
                "col",
                "x",
                "y",
                "z_terrain_m",
                "z_building_m",
                "z_total_m",
            ],
            "derived_operational_columns": [
                "z_cm",
            ],
            "relationships": [
                "z_total_m = z_terrain_m + z_building_m",
                "z_cm = f(z_total_m)",
            ],
        },
        "grid": {
            "cells_are_square": True,
            "urban_centered": True,
            "best_square_grid_required": True,
            "quadrícula_is_not_bounding_box": True,
            "bounding_box_without_envelope_is_not_valid_domain": True,
            "outside_value": "NaN",
            "nan_meaning": "no_drone_survey",
            "survey_year": 2018,
        },
        "table": {
            "prototype_shape": {
                "rows": 8,
                "cols": 16,
                "pins": 128,
            },
            "cell_cm": [
                1,
                2,
            ],
            "max_z_cm": 10.0,
            "future_mode": "MxN",
            "actuation": {
                "point": "centroid",
                "cells_are_square": True,
            },
            "scan": {
                "mode": "zigzag",
                "sequence_example": [
                    "(0,0)",
                    "(0,7)",
                    "(1,7)",
                    "(1,0)",
                    "...",
                    "(7,0)",
                ],
            },
            "transform": {
                "origin_translation": "bottom_left_to_top_right",
                "rotation_deg_clockwise": 90,
                "mapping": {
                    "x_prime": "y_rotated",
                    "y_prime": "x_rotated",
                    "z_prime": "z",
                },
            },
        },
        "geometry": {
            "rotation_parametric": True,
            "horizontal_scale_parameterized": True,
            "vertical_scale_parameterized": True,
            "north_tilt_angle_parameterized": True,
            "rotation_traceability_required": True,
            "pca_fit": {
                "pca_is_principal_orientation_line": True,
                "rotation_may_be_determined_by_pca_vs_grid": True,
                "description": "O PCA \u00e9 entendido como a linha principal cuja interse\u00e7\u00e3o/rela\u00e7\u00e3o com a quadr\u00edcula pode determinar a rota\u00e7\u00e3o, se necess\u00e1rio.",
            },
            "rotation_models": {
                "geospatial": {
                    "angle_deg": 154.63,
                    "source": "utm_alignment",
                    "precision": "2_decimal_places",
                },
                "physical_table": {
                    "angle_deg": 146.82,
                    "source": "grid_fit",
                },
                "delta_deg": 7.81,
            },
            "rotation_state": {
                "current_frame": {
                    "name": "scientific_xy",
                    "current_pca_deg": 0.0,
                    "residual_rotation_needed_deg": 0.0,
                    "already_aligned": True,
                },
                "historical_models": {
                    "geospatial_alignment": {
                        "source_orientation_deg": 154.63,
                        "applied_rotation_deg": -154.63,
                        "target_pca_deg": 0.0,
                        "source": "utm_alignment",
                    },
                    "physical_table_fit": {
                        "source_orientation_deg": 146.82,
                        "applied_rotation_deg": -146.82,
                        "target_pca_deg": 0.0,
                        "source": "grid_fit",
                    },
                },
                "delta_between_historical_models_deg": 7.81,
            },
        },
        "temporal": {
            "x_axis_can_be_temporal": True,
            "time_start_year": 1940,
            "time_end_year": 2020,
            "time_step_years": 5,
            "year_bands_define_ipt_phases": True,
            "description": "A rota\u00e7\u00e3o pode ser \u00fatil porque o eixo x passa a representar o tempo.",
        },
        "domain": {
            "official_domain_source": "urban_envelope",
            "outside_valid_domain_should_be_nan": True,
            "nan_means_no_drone_photogrammetric_survey": True,
            "drone_surface_survey_reference_year": 2018,
            "urbanization_must_be_centered_in_grid": True,
        },
        "contours": {
            "source": "DTM",
            "scope": "inside_urbanism_envelope",
            "cota_zero_definition": "minimum_DTM_within_urbanism_area",
            "derived_from_cota_zero": True,
        },
        "dxf": {
            "is_input": True,
            "can_be_reference_layer": True,
            "can_be_watermark": True,
            "used_for_validation": True,
            "can_validate_height_building_coherence": True,
        },
        "derivation": {
            "chain": [
                "DTM -> z_terrain_m",
                "DSM/NDSM -> z_building_m",
                "z_terrain_m + z_building_m -> z_total_m",
                "z_total_m -> z_cm",
                "z_cm -> mesa / bmp / grayscale / csv derivado / runtime",
            ],
        },
        "runtime": {
            "mesa_real_on_implies_immediate_sync": True,
            "virtual_table_and_physical_table_must_be_in_sync": True,
        },
        "strategic_scope": {
            "project_role": "critical_pilot",
            "future_target": "Twin City",
            "deployment_context": "Operations and Control Center",
            "future_multivariable_support": True,
            "future_carbon_related_variables": True,
        },
        "validation_policy": {
            "block_on_error": True,
            "block_on_contract_additive_required": False,
            "emit_warning": True,
            "emit_todo_contract": True,
            "emit_contract_additive_required": True,
        },
        "pending_formalization": [
            {
                "rule_id": "FORM-001",
                "title": "Mapeamento matem\u00e1tico completo entre UTM, cartesiano e mesa",
                "description": "Falta consolidar em especifica\u00e7\u00e3o \u00fanica as f\u00f3rmulas e par\u00e2metros entre os tr\u00eas sistemas.",
            },
            {
                "rule_id": "FORM-002",
                "title": "Valida\u00e7\u00e3o geom\u00e9trica expl\u00edcita de NaN fora do envelope",
                "description": "A regra existe, mas o validador ainda precisa cruzar grid cient\u00edfico com m\u00e1scara/envelope oficial.",
            },
            {
                "rule_id": "FORM-003",
                "title": "Escolha algor\u00edtmica da melhor quadr\u00edcula quadrada",
                "description": "A regra est\u00e1 definida conceitualmente, mas ainda precisa de formaliza\u00e7\u00e3o algor\u00edtmica centralizada.",
            },
            {
                "rule_id": "FORM-004",
                "title": "Contrato temporal completo da constru\u00e7\u00e3o do IPT",
                "description": "A camada temporal est\u00e1 presente no sistema, mas ainda n\u00e3o foi fundida em especifica\u00e7\u00e3o \u00fanica.",
            },
        ],
        "contract_additives_watchlist": [
            {
                "rule_id": "ADD-001",
                "title": "Rota\u00e7\u00e3o parametrizada por fase e melhor encaixe",
                "impact": "CR\u00cdTICO",
                "description": "O hist\u00f3rico mostra coexist\u00eancia de rota\u00e7\u00f5es ~146 e ~154 em fases distintas.",
                "proposed_contract_additive": "O \u00e2ngulo de rota\u00e7\u00e3o deve ser tratado como par\u00e2metro versionado por fase e por crit\u00e9rio de melhor encaixe com a quadr\u00edcula.",
            },
            {
                "rule_id": "ADD-002",
                "title": "Envelope versus bounding-box",
                "impact": "ALTO",
                "description": "Bounding-box n\u00e3o pode ser tratada como dom\u00ednio v\u00e1lido sem envelope.",
                "proposed_contract_additive": "O envelope urbano define o dom\u00ednio efetivo do sistema.",
            },
            {
                "rule_id": "ADD-003",
                "title": "Escalas e inclina\u00e7\u00e3o do norte como par\u00e2metros expl\u00edcitos",
                "impact": "ALTO",
                "description": "O sistema deve registrar escala horizontal, escala vertical, \u00e2ngulo de rota\u00e7\u00e3o e inclina\u00e7\u00e3o do norte.",
                "proposed_contract_additive": "As transforma\u00e7\u00f5es geom\u00e9tricas devem registrar escala horizontal, escala vertical, \u00e2ngulo de rota\u00e7\u00e3o e inclina\u00e7\u00e3o do norte.",
            },
            {
                "rule_id": "ADD-004",
                "title": "Sem\u00e2ntica formal de NaN fora do dom\u00ednio",
                "impact": "CR\u00cdTICO",
                "description": "NaN fora da \u00e1rea v\u00e1lida significa aus\u00eancia de levantamento aerofotogram\u00e9trico por drone.",
                "proposed_contract_additive": "Valores NaN fora da \u00e1rea v\u00e1lida indicam aus\u00eancia de levantamento aerofotogram\u00e9trico por drone e n\u00e3o devem ser tratados como zero.",
            },
            {
                "rule_id": "ADD-005",
                "title": "DXF como entrada oficial de valida\u00e7\u00e3o",
                "impact": "ALTO",
                "description": "O DXF \u00e9 entrada oficial e pode validar coer\u00eancia entre altura e edifica\u00e7\u00e3o.",
                "proposed_contract_additive": "O DXF de refer\u00eancia em CAD \u00e9 entrada oficial do sistema e pode atuar como layer, marca d'\u00e1gua e valida\u00e7\u00e3o geom\u00e9trica/sem\u00e2ntica.",
            },
        ],
    }