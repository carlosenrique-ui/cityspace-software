from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pandas as pd

from offline.validation.contract_registry import build_contract
from offline.validation.models.validation_result import ValidationLevel, ValidationResult


def ok(rule_id, title, description, evidence=None):
    return ValidationResult(
        level=ValidationLevel.OK,
        rule_id=rule_id,
        title=title,
        description=description,
        evidence=evidence,
    )


def warning(rule_id, title, description, evidence=None, impact=None, recommendation=None):
    return ValidationResult(
        level=ValidationLevel.WARNING,
        rule_id=rule_id,
        title=title,
        description=description,
        evidence=evidence,
        impact=impact,
        recommendation=recommendation,
    )


def error(rule_id, title, description, evidence=None, impact=None, recommendation=None):
    return ValidationResult(
        level=ValidationLevel.ERROR,
        rule_id=rule_id,
        title=title,
        description=description,
        evidence=evidence,
        impact=impact,
        recommendation=recommendation,
    )


def todo(rule_id, title, description):
    return ValidationResult(
        level=ValidationLevel.TODO_CONTRACT,
        rule_id=rule_id,
        title=title,
        description=description,
        impact="MÉDIO",
        recommendation="Formalizar esta regra e evoluir o validador.",
    )


def additive(rule_id, title, description, impact, recommendation, proposed_contract_additive, evidence=None):
    return ValidationResult(
        level=ValidationLevel.CONTRACT_ADDITIVE_REQUIRED,
        rule_id=rule_id,
        title=title,
        description=description,
        evidence=evidence,
        impact=impact,
        recommendation=recommendation,
        proposed_contract_additive=proposed_contract_additive,
    )


def summarize(results):
    counts = Counter(r.level.value for r in results)
    return {
        "OK": counts.get("OK", 0),
        "WARNING": counts.get("WARNING", 0),
        "ERROR": counts.get("ERROR", 0),
        "TODO-CONTRACT": counts.get("TODO-CONTRACT", 0),
        "CONTRACT-ADDITIVE-REQUIRED": counts.get("CONTRACT-ADDITIVE-REQUIRED", 0),
    }


def validate_csv_presence(contract):
    results = []
    csv_path = Path(contract["paths"]["scientific_grid_csv"])

    if csv_path.exists():
        results.append(ok(
            "DATA-000",
            "CSV científico presente",
            "Arquivo científico canônico encontrado.",
            evidence=str(csv_path),
        ))
    else:
        results.append(error(
            "DATA-000",
            "CSV científico ausente",
            "Arquivo científico canônico não encontrado.",
            evidence=str(csv_path),
            impact="CRÍTICO",
            recommendation="Gerar offline/products/scientific/grid_metrics_utm.csv",
        ))
    return results


def validate_data_schema(df, contract):
    results = []

    base_columns = contract["data_schema"]["base_scientific_columns"]
    derived_columns = contract["data_schema"]["derived_operational_columns"]

    missing_base = [c for c in base_columns if c not in df.columns]
    present_derived = [c for c in derived_columns if c in df.columns]
    missing_derived = [c for c in derived_columns if c not in df.columns]

    if missing_base:
        results.append(error(
            "DATA-001",
            "Schema científico base incompleto",
            "Colunas científicas base ausentes.",
            evidence={"missing": missing_base, "found": list(df.columns)},
            impact="CRÍTICO",
            recommendation="Corrigir o CSV científico base.",
        ))
        return results

    results.append(ok(
        "DATA-001",
        "Schema científico base válido",
        "Colunas científicas base presentes.",
        evidence={"columns": base_columns},
    ))

    if "z_terrain_m" in df.columns and "z_building_m" in df.columns and "z_total_m" in df.columns:
        total_expected = df["z_terrain_m"] + df["z_building_m"]
        diff = (df["z_total_m"] - total_expected).abs()
        bad = int((diff > 1e-6).sum())

        if bad > 0:
            results.append(error(
                "DATA-002",
                "Relação z_total_m inconsistente",
                "z_total_m difere de z_terrain_m + z_building_m.",
                evidence={"bad_rows": bad},
                impact="CRÍTICO",
                recommendation="Corrigir a derivação da altura total.",
            ))
        else:
            results.append(ok(
                "DATA-002",
                "Relação z_total_m consistente",
                "z_total_m = z_terrain_m + z_building_m.",
            ))

    if present_derived:
        results.append(ok(
            "DATA-003",
            "Colunas operacionais derivadas presentes",
            "O CSV já contém colunas operacionais derivadas.",
            evidence={"present": present_derived},
        ))
    else:
        results.append(todo(
            "DATA-003",
            "z_cm ainda não presente no CSV científico base",
            "z_cm foi tratado como derivação operacional posterior, não como coluna obrigatória do CSV base atual.",
        ))

    if "x" in df.columns and "y" in df.columns:
        results.append(ok(
            "DATA-004",
            "Coordenadas científicas x/y presentes",
            "O CSV científico contém x e y no sistema científico/intermediário.",
            evidence={"columns": ["x", "y"]},
        ))

    return results


def validate_grid_and_table(df, contract):
    results = []

    if "row" not in df.columns or "col" not in df.columns:
        results.append(error(
            "GRID-000",
            "row/col ausentes",
            "Não é possível validar malha sem row e col.",
            impact="CRÍTICO",
            recommendation="Garantir presença de row e col no CSV científico.",
        ))
        return results

    dup = int(df.duplicated(subset=["row", "col"]).sum())
    if dup > 0:
        results.append(error(
            "GRID-001",
            "Duplicidade row/col",
            "Foram encontradas células duplicadas.",
            evidence={"duplicate_rows": dup},
            impact="CRÍTICO",
            recommendation="Garantir unicidade da chave lógica row/col.",
        ))
    else:
        results.append(ok(
            "GRID-001",
            "Sem duplicidade row/col",
            "Cada célula possui chave row/col única.",
        ))

    rows = len(df["row"].dropna().unique())
    cols = len(df["col"].dropna().unique())

    proto = contract["table"]["prototype_shape"]
    expected_rows = int(proto["rows"])
    expected_cols = int(proto["cols"])

    if (rows, cols) == (expected_rows, expected_cols):
        results.append(ok(
            "TABLE-001",
            "Malha default detectada",
            "Malha atual corresponde ao protótipo default.",
            evidence={"rows": rows, "cols": cols},
        ))
    else:
        results.append(additive(
            "TABLE-001",
            "Malha diferente do default",
            "A malha encontrada não coincide com o protótipo atual.",
            impact="ALTO",
            recommendation="Confirmar se já é um caso de generalização MxN.",
            proposed_contract_additive="A mesa deve suportar generalização MxN mantendo a malha atual apenas como default histórico.",
            evidence={"rows": rows, "cols": cols},
        ))

    if contract["grid"]["cells_are_square"]:
        results.append(ok(
            "TABLE-002",
            "Contrato de células quadradas ativo",
            "A mesa é tratada por contrato como formada por células quadradas.",
        ))

    scan_mode = contract["table"]["scan"]["mode"]
    if scan_mode == "zigzag":
        results.append(ok(
            "TABLE-003",
            "Contrato de varredura zigzag ativo",
            "A ordem operacional da mesa é zigzag.",
            evidence={"scan_mode": scan_mode},
        ))

    if contract["table"]["actuation"]["point"] == "centroid":
        results.append(ok(
            "TABLE-004",
            "Contrato de atuação no centroide ativo",
            "O acionador atua no centroide da célula.",
        ))

    return results


def validate_geometry(contract):
    results = []

    ref_names = [x["name"] for x in contract["reference_systems"]["mandatory"]]
    expected = ["utm", "cartesian_trigonometric", "physical_table"]
    if ref_names == expected:
        results.append(ok(
            "REF-001",
            "Sistemas de referência oficiais definidos",
            "UTM, cartesiano trigonométrico e mesa física estão explicitamente definidos.",
            evidence=ref_names,
        ))
    else:
        results.append(error(
            "REF-001",
            "Sistemas de referência inconsistentes",
            "Os sistemas de referência oficiais não coincidem com o contrato esperado.",
            evidence=ref_names,
            impact="CRÍTICO",
            recommendation="Corrigir a definição dos sistemas de referência no contract_registry.py",
        ))

    rot_hist = contract["geometry"]["rotation_history"]
    results.append(additive(
        "GEO-001",
        "Rotação histórica versionada",
        "O sistema tem histórico de rotações ~146 e ~154, o que exige parâmetro versionado por fase.",
        impact="CRÍTICO",
        recommendation="Formalizar rotação por fase/objetivo no contrato e no pipeline.",
        proposed_contract_additive="Ângulos de rotação devem ser tratados como parâmetros versionados e auditáveis, não constantes cegas.",
        evidence=rot_hist,
    ))

    if contract["geometry"]["pca_fit"]["pca_is_principal_orientation_line"]:
        results.append(ok(
            "GEO-002",
            "PCA como linha principal de orientação",
            "O contrato reconhece PCA como linha principal para decisão de rotação/encaixe.",
        ))

    if contract["geometry"]["horizontal_scale_parameterized"] and contract["geometry"]["vertical_scale_parameterized"]:
        results.append(additive(
            "GEO-003",
            "Escalas horizontal e vertical parametrizadas",
            "As escalas são parâmetros explícitos do contrato, mas ainda não estão validadas automaticamente.",
            impact="ALTO",
            recommendation="Ligar validação de escala ao pipeline e aos metadados.",
            proposed_contract_additive="As transformações geométricas devem registrar escala horizontal e vertical como parâmetros auditáveis.",
        ))

    if contract["geometry"]["north_tilt_angle_parameterized"]:
        results.append(additive(
            "GEO-004",
            "Inclinação do norte parametrizada",
            "O ângulo de inclinação do norte é parâmetro explícito, mas ainda não é validado automaticamente.",
            impact="ALTO",
            recommendation="Registrar e validar north_tilt_angle_deg nos metadados.",
            proposed_contract_additive="As transformações geométricas devem registrar inclinação do norte como parâmetro auditável.",
        ))

    return results


def validate_domain_and_contours(contract):
    results = []

    if contract["domain"]["official_domain_source"] == "urban_envelope":
        results.append(additive(
            "DOMAIN-001",
            "Envelope versus bounding-box",
            "O domínio válido deve ser envelope urbano, não bounding-box puro.",
            impact="ALTO",
            recommendation="Formalizar distinção no contrato e validar no pipeline.",
            proposed_contract_additive="Bounding-box não é domínio válido sem envelope; o envelope urbano define o domínio efetivo do sistema.",
        ))

    if contract["domain"]["outside_valid_domain_should_be_nan"]:
        results.append(todo(
            "DOMAIN-002",
            "NaN fora do domínio",
            "A regra existe, mas a validação geométrica explícita contra envelope ainda não foi ligada.",
        ))

    if contract["domain"]["nan_means_no_drone_photogrammetric_survey"]:
        results.append(additive(
            "DOMAIN-003",
            "Semântica formal de NaN",
            "NaN fora da área válida significa ausência de levantamento aerofotogramétrico por drone.",
            impact="CRÍTICO",
            recommendation="Preservar essa semântica e bloquear conversões indevidas para zero.",
            proposed_contract_additive="Valores NaN fora da área válida indicam ausência de levantamento aerofotogramétrico por drone e não devem ser tratados como zero.",
            evidence={"survey_year": contract["domain"]["drone_surface_survey_reference_year"]},
        ))

    if contract["contours"]["source"] == "DTM":
        results.append(ok(
            "CONTOUR-001",
            "Contours derivados do DTM",
            "O contrato define que contours derivam do DTM.",
        ))

    if contract["contours"]["derived_from_cota_zero"]:
        results.append(additive(
            "CONTOUR-002",
            "Cota zero local para contours",
            "Contours derivam da menor cota do DTM dentro do urbanismo.",
            impact="ALTO",
            recommendation="Formalizar e validar essa derivação no pipeline.",
            proposed_contract_additive="A cota zero dos contours deve ser definida pela menor cota do DTM dentro do urbanismo.",
        ))

    return results


def validate_temporal_and_runtime(contract):
    results = []

    temporal = contract["temporal"]
    if temporal["x_axis_can_be_temporal"]:
        results.append(ok(
            "TEMP-001",
            "Eixo x temporal reconhecido",
            "O contrato reconhece que o eixo x pode representar o tempo.",
            evidence={
                "start": temporal["time_start_year"],
                "end": temporal["time_end_year"],
                "step": temporal["time_step_years"],
            },
        ))

    results.append(todo(
        "TEMP-002",
        "Contrato temporal completo ainda não validado",
        "As faixas históricas do IPT ainda não estão sendo validadas automaticamente no runtime.",
    ))

    if contract["runtime"]["mesa_real_on_implies_immediate_sync"]:
        results.append(todo(
            "SYNC-001",
            "Sincronismo UI/mesa real",
            "A regra existe, mas a validação automática ainda não foi integrada ao runtime físico.",
        ))

    return results


def validate_dxf(contract):
    results = []

    if contract["dxf"]["is_input"]:
        results.append(ok(
            "DXF-001",
            "DXF reconhecido como entrada oficial",
            "O DXF de referência em CAD é tratado como entrada oficial do sistema.",
        ))

    if contract["dxf"]["can_validate_height_building_coherence"]:
        results.append(additive(
            "DXF-002",
            "DXF como validador de coerência altura ↔ edificação",
            "O DXF pode validar coerência entre altura e presença de prédio.",
            impact="ALTO",
            recommendation="Conectar checagem DXF ↔ alturas ao pipeline.",
            proposed_contract_additive="O DXF de referência pode atuar como validação geométrica e semântica entre altura e edificação.",
        ))

    return results


def validate_watchlists(contract):
    results = []

    for item in contract.get("pending_formalization", []):
        results.append(todo(
            item["rule_id"],
            item["title"],
            item["description"],
        ))

    for item in contract.get("contract_additives_watchlist", []):
        results.append(additive(
            item["rule_id"],
            item["title"],
            item["description"],
            impact=item["impact"],
            recommendation="Confirmar com Carlos se deve virar aditivo oficial do contrato.",
            proposed_contract_additive=item["proposed_contract_additive"],
        ))

    return results


def write_report(base_dir: Path, results):
    out_dir = base_dir / "offline" / "validation" / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "contract_report.json"

    payload = {
        "summary": summarize(results),
        "details": [r.to_dict() for r in results],
    }

    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def validate(base_dir: Path):
    contract = build_contract(base_dir)
    results = []

    results.extend(validate_csv_presence(contract))

    csv_path = Path(contract["paths"]["scientific_grid_csv"])
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        results.extend(validate_data_schema(df, contract))
        results.extend(validate_grid_and_table(df, contract))

    results.extend(validate_geometry(contract))
    results.extend(validate_domain_and_contours(contract))
    results.extend(validate_temporal_and_runtime(contract))
    results.extend(validate_dxf(contract))
    results.extend(validate_watchlists(contract))

    return results, contract


def main():
    base_dir = Path(".").resolve()
    results, _contract = validate(base_dir)
    out_path = write_report(base_dir, results)

    print("\n================ CONTRACT VALIDATION SUMMARY ================")
    for k, v in summarize(results).items():
        print(f"{k}: {v}")

    print(f"\n[OK] Report written to: {out_path}")

    has_error = any(r.level == ValidationLevel.ERROR for r in results)
    raise SystemExit(2 if has_error else 0)


if __name__ == "__main__":
    main()
