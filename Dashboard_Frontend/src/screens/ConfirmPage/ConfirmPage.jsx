import React from "react";
import "./style.css";

export const ConfirmPage = ({ onConfirm, onClose }) => {
  return (
    <div className="confirm-page-overlay" onClick={onClose}>
      <div className="confirm-page" onClick={(e) => e.stopPropagation()}>
        <div className="overlap-wrapper-2">
          <div className="overlap-47">
            <div className="group-44">
              <div className="overlap-48">
                <div className="group-45">
                  <div className="overlap-49">
                    <div className="rectangle-33" />
                    <div className="rectangle-34" />

                    <p className="text-wrapper-118">Notifying the Cleaning Staff!</p>
                    <div className="text-wrapper-119">Estimated Time:</div>
                    <div className="text-wrapper-121">10:00</div>

                    {/* ✅ Confirm Button */}
                    <div className="frame-7" onClick={onConfirm}>
                      <div className="frame-8">
                        <div className="overlap-group-16">
                          <div className="rectangle-35" />
                          <div className="text-wrapper-120">Confirm</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* ✅ Success Check Icon */}
                <div className="on-track-8">
                  <div className="frame-9">
                    <img className="done-3" alt="Done" src="/img/done-17.png" />
                  </div>
                </div>

                {/* ✅ Close Button */}
                <button className="close-button" onClick={onClose}>
                  <img className="group-46" alt="Group" src="/img/group-18.png" />
                </button>

                <img className="web-brand-logo-4" alt="Web brand logo" src="/img/web-brand-logo-horizontal-blue-rgb-2.png" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
