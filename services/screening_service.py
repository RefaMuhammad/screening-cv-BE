import os
from models.schemas import JobRequirement, Gate1Result
from services.cv_parser import CVParser
from services.rule_engine import RuleEngine
from typing import List

async def process_batch(job_req: JobRequirement, file_paths: List[str]) -> List[Gate1Result]:
    parser = CVParser()
    engine = RuleEngine()
    results = []

    for filepath in file_paths:
        try:
            filename = os.path.basename(filepath)
            print(f"\n{'='*50}")
            print(f"[START] Processing CV: {filename}")
            print(f"{'='*50}")

            # 1. Parse CV to CandidateInfo
            job_desc_text = job_req.role_description.overview if job_req.role_description else ""
            parsed_data = parser.process_cv(filepath, job_desc_text)
            candidate_info = parsed_data["candidate_info"]
            
            # 2. Run Gate 1 Rule Engine
            result = engine.evaluate(candidate_info, job_req, filename)
            results.append(result)
            
            print(f"[FINISHED] Gate 1 for {filename} -> Result: {result.status}")
            
        except Exception as e:
            print(f"[ERROR] Failed processing {filepath}: {e}")
            filename = os.path.basename(filepath)
            # Create a mock error result so batch doesn't fail entirely
            # We don't have a perfect schema fit for errors, but we can return FAIL
            from models.schemas import Gate1Criteria, CriteriaResult
            
            err_crit = CriteriaResult(status="FAIL", required="N/A", actual="Error", reason=str(e))
            results.append(Gate1Result(
                candidate_name="Unknown",
                filename=filename,
                status="ERROR",
                criteria=Gate1Criteria(
                    experience=err_crit,
                    skills=err_crit,
                    language=err_crit,
                    visa=err_crit
                ),
                overall_reason=f"Processing failed: {str(e)}",
                evidence_snippets=[]
            ))
            
    return results
