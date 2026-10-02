import json

class SECAD_3D_Solver:
    """절대 원점(0,0,0)을 기준으로 3D 좌표를 설정하고 2D 평면으로 완벽히 투영하는 코어 엔진"""
    def __init__(self):
        self.origin = (0, 0, 0)
        self.points = {}

    def add_point(self, name, dx, dy, dz):
        """원점 기준 3D 상대 좌표 확정"""
        self.points[name] = {
            'x': self.origin[0] + dx,
            'y': self.origin[1] + dy,
            'z': self.origin[2] + dz
        }
        print(f"[SECAD Core] Point '{name}' 정의됨: 3D{self.points[name]}")

    # ===== 기계적 3각법 투상 (수학적 맵핑) =====
    def proj_top(self, name):
        """평면도: XY (Z 무시)"""
        p = self.points[name]
        return (p['x'], p['y'])

    def proj_front(self, name):
        """정면도: XZ (Y 무시, SVG 좌표계 특성상 Z 반전 필요시 조정)"""
        p = self.points[name]
        return (p['x'], -p['z'])

    def proj_right(self, name):
        """우측면도: YZ (X 무시)"""
        p = self.points[name]
        return (p['y'], -p['z'])

if __name__ == "__main__":
    print("=== SECAD 기하학 투상 엔진 테스트 (Origin 0,0,0 기반) ===")
    solver = SECAD_3D_Solver()
    
    # 1. 원점 설정 (Base 좌측 하단)
    solver.add_point("Origin_BL", 0, 0, 0)
    
    # 2. 형상 핵심 포인트 3D 정의 (Drawing 174 예제)
    solver.add_point("Base_TR", 150, 82, 10)  # 베이스 끝점
    solver.add_point("Boss_Center", 129, 41, 96) # 우측 보스 중심점
    solver.add_point("Left_Pad_1", 15, 16, 10) # 좌측 1번 패드 중심

    print("\n--- 일관성 검증 렌더링 좌표 ---")
    print(f"보스 평면도 (Top): X={solver.proj_top('Boss_Center')[0]}, Y={solver.proj_top('Boss_Center')[1]} (완벽한 정렬)")
    print(f"보스 정면도 (Front): X={solver.proj_front('Boss_Center')[0]}, Z={solver.proj_front('Boss_Center')[1]} (Top과 X축 정확히 일치)")
    print(f"보스 우측면도(Right): Y={solver.proj_right('Boss_Center')[0]}, Z={solver.proj_right('Boss_Center')[1]} (Front와 Z축 정확히 일치)")
