import React, { useState, useEffect } from "react";
import { LargeInput } from "../../components/LargeInput";
import { Sidebar } from "../../components/Sidebar";
import { ActiveAlerts } from "../ActiveAlerts/ActiveAlerts";
import "./style.css";

export const ElevatorStatus = () => {

  const [modalOpen, setModalOpen] = useState(false);

  return (
    <div className="report-logs">
      <div className="div-5">
        <div className="text-wrapper-58">Hi Andrei,</div>

        <p className="text-wrapper-59">Find Elevator Sensor Status Here</p>

        <div className="overlap-20">
          <Sidebar activePage="Elevator Status" 
          />

          <div className="noun-status">
            <div className="overlap-21">
              <div className="text-wrapper-60">Created by Larea</div>

              <div className="text-wrapper-61">from the Noun Project</div>
            </div>
          </div>
        </div>

        <p className="current-time-PM">
          Current
          Time:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1:44
          PM&nbsp;&nbsp;&nbsp;&nbsp;Jan 30 2025
        </p>

        <LargeInput
          captionTextClassName="large-input-3"
          className="large-input-instance"
          overlapClassName="large-input-2"
          state="default"
          type="search-icon"
        />
        <div className="group-22">
          <div className="overlap-22">
            <img className="vector-16" alt="Vector" src="/img/vector.png" />

            <div className="text-wrapper-62">UW&nbsp;&nbsp;Station</div>
          </div>

          <div className="overlap-23">
            <img className="vector-17" alt="Vector" src="/img/vector.png" />

            <div className="line-4">Line&nbsp;&nbsp; 1</div>
          </div>

          <div className="overlap-24">
            <div className="text-wrapper-62">Elevator&nbsp;&nbsp;——</div>

            <img className="vector-18" alt="Vector" src="/img/vector.png" />
          </div>
        </div>

        <div className="overlap-25">
          <div className="text-wrapper-63">Line</div>

          <div className="text-wrapper-64">Station</div>

          <div className="elevator-3"> Elevator</div>

          <div className="text-wrapper-65">Status</div>

          <div className="text-wrapper-66">Sensor</div>

          <div className="group-23">
            <div className="overlap-26">
              <div className="text-wrapper-67">Line 1</div>

              <div className="text-wrapper-68">Lynnwood City Center</div>
            </div>

            <div className="text-wrapper-69">Line 1</div>

            <div className="overlap-27">
              <div className="text-wrapper-67">Line 1</div>

              <div className="text-wrapper-68">Mountlake Terrace</div>
            </div>

            <div className="overlap-28">
              <div className="text-wrapper-70">Line 1</div>

              <div className="text-wrapper-68">Shoreline South/148th</div>
            </div>

            <div className="overlap-29">
              <div className="text-wrapper-67">Line 1</div>

              <div className="text-wrapper-68">Northgate</div>
            </div>

            <div className="text-wrapper-71">23</div>

            <div className="text-wrapper-72">24</div>

            <div className="text-wrapper-73">25</div>

            <div className="text-wrapper-74">26</div>

            <div className="text-wrapper-75">27</div>

            <div className="text-wrapper-76">Shoreline North/185th</div>

            <div className="depth-frame-9">
              <div className="depth-frame-10">
                <div className="text-wrapper-77">Good</div>
              </div>
            </div>

            <div className="depth-frame-11">
              <div className="depth-frame-10">
                <div className="text-wrapper-77">Good</div>
              </div>
            </div>

            <div className="depth-frame-12">
              <div className="depth-frame-10">
                <div className="text-wrapper-77">Good</div>
              </div>
            </div>

            <div className="depth-frame-13">
              <div className="depth-frame-10">
                <div className="text-wrapper-77">Good</div>
              </div>
            </div>

            <div className="depth-frame-14">
              <div className="depth-frame-10">
                <div className="text-wrapper-77">Good</div>
              </div>
            </div>

            <div className="depth-frame-15">
              <div className="depth-frame-10">
                <div className="text-wrapper-77">Good</div>
              </div>
            </div>

            <div className="depth-frame-16">
              <div className="depth-frame-10">
                <div className="text-wrapper-77">Processing</div>
              </div>
            </div>

            <div className="depth-frame-17">
              <div className="depth-frame-10">
                <div className="text-wrapper-77">Processing</div>
              </div>
            </div>

            <div className="depth-frame-18">
              <div className="depth-frame-10">
                <div className="text-wrapper-77">Processing</div>
              </div>
            </div>

            <div className="depth-frame-19">
              <div className="depth-frame-10">
                <div className="text-wrapper-77">Processing</div>
              </div>
            </div>

            <img className="vector-19" alt="Vector" src="/img/vector-3-1.png" />

            <img className="vector-20" alt="Vector" src="/img/vector-3-1.png" />

            <img className="vector-21" alt="Vector" src="/img/vector-3-1.png" />

            <img className="vector-22" alt="Vector" src="/img/vector-3-1.png" />

            <img className="vector-23" alt="Vector" src="/img/vector-3-1.png" />

            <img className="vector-24" alt="Vector" src="/img/vector-3-1.png" />
          </div>
        </div>

        <ActiveAlerts isOpen={modalOpen} onClose={() => setModalOpen(false)} />
        <div className="group-24" >
          <div className="overlap-30" onClick={() => setModalOpen(true)}>
            <img className="vector-25" alt="Vector" src="/img/vector-3.png" />

            <div className="group-25" />

            <div className="text-wrapper-78">4</div>
          </div>
        </div>
      </div>
    </div>
  );
};
